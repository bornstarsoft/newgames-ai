#!/usr/bin/env python3
"""Validate original teaching examples and their generated, script-free article."""
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from check_updates import Page


class Exercises(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.examples, self.current, self.cell = {}, None, None
        self.text = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and attrs.get("class") == "sudoku-check":
            self.current = attrs["id"]
            self.examples[self.current] = {"digits": [], "details": 0, "summary": 0}
        if self.current:
            if tag == "td":
                self.cell = ""
            if tag == "details":
                assert "open" not in attrs, "Answers should start collapsed"
                self.examples[self.current]["details"] += 1
            if tag == "summary":
                self.examples[self.current]["summary"] += 1

    def handle_data(self, data):
        self.text.append(data)
        if self.cell is not None:
            self.cell += data

    def handle_endtag(self, tag):
        if tag == "td" and self.current:
            self.examples[self.current]["digits"].append([int(n.strip()) for n in self.cell.split(",")])
            self.cell = None
        if tag == "section":
            self.current = None


def main():
    root = Path(__file__).resolve().parent.parent
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "public"
    data = json.loads((root / "data/sudoku_practice.json").read_text())
    # A constructed valid reference checks that the overlapping clue groups agree.
    board = [[(r * 3 + r // 3 + c) % 9 + 1 for c in range(9)] for r in range(9)]
    digits = set(range(1, 10))
    route = "/blog/how-to-find-your-first-sudoku-move/"
    path = public / route.lstrip("/") / "index.html"
    page = Page(path)
    parsed = Exercises(path.read_text())
    assert len(data) == len(parsed.examples) == 3
    for key, item in data.items():
        r, c = item["cell"]
        groups = {
            "row": [(r, x) for x in range(9) if x != c],
            "column": [(y, c) for y in range(9) if y != r],
            "box": [(y, x) for y in range(r // 3 * 3, r // 3 * 3 + 3)
                    for x in range(c // 3 * 3, c // 3 * 3 + 3) if (y, x) != (r, c)],
        }
        clues = set()
        for name, cells in groups.items():
            assert len(item[name]) == len(set(item[name]))
            assert set(item[name]) <= {board[y][x] for y, x in cells}
            clues.update((y, x) for y, x in cells if board[y][x] in item[name])
        for name, cells in groups.items():
            assert set(item[name]) == {board[y][x] for y, x in cells if (y, x) in clues}, (key, name)
        remaining = sorted(digits - set(item["row"]) - set(item["column"]) - set(item["box"]))
        assert remaining == item["candidates"], key
        rendered = parsed.examples["check-" + key]
        assert rendered["digits"] == [item[n] for n in ("row", "column", "box")]
        assert rendered["details"] == rendered["summary"] == 1
        assert item["answer"] in " ".join(parsed.text)
        assert item["reason"] in " ".join(parsed.text)
    assert data["one-left"]["candidates"] == [5]
    assert data["cross-check"]["candidates"] == [3]
    assert data["not-yet"]["candidates"] == [2, 3]
    assert page.canonical == "https://newgames.ai" + route
    assert page.meta["robots"] == "index,follow"
    assert all(s.get("type") == "application/ld+json" for s in page.scripts)
    assert "/updates/#handy-guides" in page.links
    for parent in ("index.html", "updates/index.html", "puzzle-games/index.html"):
        assert route in Page(public / parent).links, parent
    assert page.canonical in {n.text for n in ET.parse(public / "sitemap.xml").iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    assert page.canonical in {n.text for n in ET.parse(public / "blog/index.xml").findall("./channel/item/link")}
    assert "sudoku-guide.css" not in (public / "index.html").read_text()
    print("PASS: three consistent original clue groups, exact candidates and rendered answers, native disclosures, metadata/discovery/sitemap/RSS, no homepage stylesheet")


if __name__ == "__main__":
    main()
