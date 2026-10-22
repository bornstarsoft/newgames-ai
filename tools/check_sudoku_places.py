#!/usr/bin/env python3
"""Check original hidden-single snapshots, rendered content and discovery links."""
from copy import deepcopy
from html.parser import HTMLParser
from itertools import permutations
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from check_updates import Page

DIGITS = set(range(1, 10))
ROUTE = "/blog/sudoku-one-place-for-a-number/"


def check_example(item):
    board = item["clues"]
    assert len(board) == 9 and all(len(row) == 9 for row in board)
    # Every clue agrees with a constructed complete Sudoku, not a copied puzzle.
    solution = [[(r * 3 + r // 3 + c) % 9 + 1 for c in range(9)] for r in range(9)]
    for r, row in enumerate(board):
        for c, digit in enumerate(row):
            assert type(digit) is int and (digit == 0 or digit == solution[r][c])
    row = item["row"]
    missing = sorted(DIGITS - set(board[row]))
    assert item["missing"] == missing
    assert item["target"] in missing
    assert [cell["column"] for cell in item["cells"]] == [c + 1 for c in range(9) if not board[row][c]]
    for cell in item["cells"]:
        c = cell["column"] - 1
        seen = set(board[row]) | {board[r][c] for r in range(9)}
        seen |= {board[r][x] for r in range(row // 3 * 3, row // 3 * 3 + 3)
                 for x in range(c // 3 * 3, c // 3 * 3 + 3)}
        assert cell["candidates"] == sorted(DIGITS - seen)
        assert len(cell["candidates"]) > 1, "These examples must not be single-candidate cells"
    places = [cell["column"] for cell in item["cells"] if item["target"] in cell["candidates"]]
    assert item["places"] == places
    # Check row assignments, without claiming uniqueness or solving an unseen game.
    assignments = [values for values in permutations(missing)
                   if all(d in cell["candidates"] for d, cell in zip(values, item["cells"]))]
    assert assignments
    possible = {item["cells"][values.index(item["target"])]["column"] for values in assignments}
    assert possible == set(places)


class Examples(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.examples = {}
        self.current = self.cell = None
        self.text = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and attrs.get("class") == "sudoku-check":
            self.current = attrs["id"]
            self.examples[self.current] = {"digits": [], "labels": [], "details": 0}
        if self.current:
            if tag == "td" or (tag == "th" and attrs.get("scope") == "row"):
                self.cell = [tag, ""]
            if tag == "details":
                assert "open" not in attrs
                self.examples[self.current]["details"] += 1

    def handle_data(self, data):
        self.text.append(data)
        if self.cell is not None: self.cell[1] += data

    def handle_endtag(self, tag):
        if self.cell is not None and tag == self.cell[0]:
            if tag == "td":
                self.examples[self.current]["digits"].append([int(n.strip()) for n in self.cell[1].split(",")])
            else:
                self.examples[self.current]["labels"].append(self.cell[1])
            self.cell = None
        if tag == "section": self.current = None


def main():
    root = Path(__file__).resolve().parent.parent
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "public"
    data = json.loads((root / "data/sudoku_places.json").read_text())
    assert set(data) == {"one-place", "two-places"}
    assert data["one-place"]["places"] == [5]
    assert data["two-places"]["places"] == [2, 5]
    path = public / ROUTE.lstrip("/") / "index.html"
    page, rendered = Page(path), Examples(path.read_text())
    assert set(rendered.examples) == {"place-" + key for key in data}
    for key, item in data.items():
        check_example(item)
        result = rendered.examples["place-" + key]
        assert result["digits"] == [cell["candidates"] for cell in item["cells"]]
        assert result["labels"] == [f"Column {cell['column']}" for cell in item["cells"]]
        assert result["details"] == 1
        assert item["answer"] in " ".join(rendered.text)
        assert item["reason"] in " ".join(rendered.text)
    for kind in ("candidate", "missing-cell", "false-place", "bad-clue"):
        bad = deepcopy(data["one-place"])
        if kind == "candidate": bad["cells"][0]["candidates"].append(5)
        if kind == "missing-cell": bad["cells"].pop()
        if kind == "false-place": bad["places"] = [2, 5]
        if kind == "bad-clue": bad["clues"][0][0] = 9
        try:
            check_example(bad)
        except AssertionError:
            pass
        else:
            raise AssertionError(f"Invalid {kind} fixture accepted")
    assert page.canonical == "https://newgames.ai" + ROUTE
    assert page.meta["robots"] == "index,follow" and "2026-10-23" in page.times
    assert all(s.get("type") == "application/ld+json" for s in page.scripts)
    assert "/blog/how-to-find-your-first-sudoku-move/" in page.links
    for parent in ("index.html", "blog/index.html", "updates/index.html", "puzzle-games/index.html",
                   "blog/how-to-find-your-first-sudoku-move/index.html"):
        assert ROUTE in Page(public / parent).links, parent
    assert page.canonical in {n.text for n in ET.parse(public / "sitemap.xml").iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    for feed in ("blog/index.xml", "updates/index.xml"):
        assert page.canonical in {n.text for n in ET.parse(public / feed).findall("./channel/item/link")}
    assert "sudoku-guide.css" in path.read_text()
    assert "sudoku-guide.css" not in (public / "index.html").read_text()
    print("PASS: two original consistent snapshots, full candidate recomputation, row assignments, four invalid fixtures rejected, rendered answers and discovery/SEO/feed links")


if __name__ == "__main__":
    main()
