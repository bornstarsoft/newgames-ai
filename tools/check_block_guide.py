#!/usr/bin/env python3
"""Validate fixed teaching boards, not a production game engine."""
from html.parser import HTMLParser
import json
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from check_updates import Page


def place(board, piece, origin):
    occupied = {(r, c) for r, row in enumerate(board) for c, value in enumerate(row) if value == "#"}
    cells = {(origin[0] + r, origin[1] + c) for r, c in piece}
    if any(not (0 <= r < 4 and 0 <= c < 4) for r, c in cells) or occupied & cells:
        return None
    occupied |= cells
    rows = [r for r in range(4) if all((r, c) in occupied for c in range(4))]
    columns = [c for c in range(4) if all((r, c) in occupied for r in range(4))]
    remaining = {(r, c) for r, c in occupied if r not in rows and c not in columns}
    return rows, columns, remaining


class Exercises(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.examples, self.current, self.cell = {}, None, None
        self.text = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and attrs.get("class") == "block-check":
            self.current = attrs["id"]
            self.examples[self.current] = {"cells": [], "scopes": [], "details": 0, "summary": 0, "caption": 0}
        if self.current:
            item = self.examples[self.current]
            if tag == "td": self.cell = ""
            if tag == "th": item["scopes"].append(attrs.get("scope"))
            if tag == "caption": item["caption"] += 1
            if tag == "details":
                assert "open" not in attrs, "Answers must start closed"
                item["details"] += 1
            if tag == "summary": item["summary"] += 1

    def handle_data(self, data):
        self.text.append(data)
        if self.cell is not None: self.cell += data

    def handle_endtag(self, tag):
        if tag == "td" and self.current:
            self.examples[self.current]["cells"].append(self.cell.strip())
            self.cell = None
        if tag == "section": self.current = None


def main():
    root = Path(__file__).resolve().parent.parent
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "public"
    data = json.loads((root / "data/block_practice.json").read_text())
    route = "/blog/block-puzzle-fit-clear-leave-space/"
    path = public / route.lstrip("/") / "index.html"
    markup = path.read_text()
    parsed, page = Exercises(markup), Page(path)
    assert set(data) == {"fit", "clear", "space"}
    assert len(parsed.examples) == 3
    text = " ".join(parsed.text)
    for key, item in data.items():
        board = item["board"]
        assert len(board) == 4 and all(len(row) == 4 and set(row) <= {"#", "."} for row in board)
        assert not any(all(board[r][c] == "#" for c in range(4)) for r in range(4))
        assert not any(all(board[r][c] == "#" for r in range(4)) for c in range(4))
        assert len(set(map(tuple, item["piece"]))) == len(item["piece"])
        for option in item["options"]:
            assert option["label"] in text
            result = place(board, item["piece"], option["origin"])
            assert (result is not None) == option["valid"], (key, option)
            if result is None: continue
            rows, columns, remaining = result
            assert rows == option["rows"] and columns == option["columns"]
            assert len(remaining) == option["remaining"]
            if "nextPiece" in item:
                fits = [[r, c] for r in range(4) for c in range(4)
                        if all(0 <= r + y < 4 and 0 <= c + x < 4 and (r + y, c + x) not in remaining
                               for y, x in item["nextPiece"])]
                assert fits == option["nextFits"], (key, option)
        rendered = parsed.examples["check-" + key]
        assert rendered["cells"] == ["X" if cell == "#" else "." for row in board for cell in row]
        assert rendered["scopes"] == ["col"] * 5 + ["row"] * 4
        assert rendered["details"] == rendered["summary"] == rendered["caption"] == 1
        assert item["answer"] in text and item["reason"] in text
    # Pin the teaching claims independently of their prose and expected-data fields.
    assert place(data["fit"]["board"], [[0, 0], [0, 1]], [1, 1]) is None
    assert place(data["fit"]["board"], [[0, 0], [0, 1]], [0, 3]) is None
    assert place(data["clear"]["board"], [[0, 0]], [0, 2]) == ([0], [2], set())
    assert data["space"]["options"][0]["nextFits"] and not data["space"]["options"][1]["nextFits"]
    assert data["space"]["options"][1]["remaining"] == 8
    assert page.canonical == "https://newgames.ai" + route
    assert page.meta["robots"] == "index,follow" and "2026-10-23" in page.times
    assert all(s.get("type") == "application/ld+json" for s in page.scripts)
    assert "block-guide.css" in markup and "guide-navigation" in markup
    assert "/blog/#learn" in page.links
    for parent in ("index.html", "blog/index.html", "updates/index.html", "puzzle-games/index.html"):
        parent_page = public / parent
        assert route in Page(parent_page).links, parent
        assert "block-guide.css" not in parent_page.read_text(), parent
    assert page.canonical in {n.text for n in ET.parse(public / "sitemap.xml").iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    assert page.canonical in {n.text for n in ET.parse(public / "blog/index.xml").findall("./channel/item/link")}
    print("PASS: 3 original 4x4 boards, 6 choices, overlap/boundary rejection, simultaneous clears, exhaustive next-piece fits, rendered cells/answers, metadata/discovery/sitemap/RSS and scoped CSS")


if __name__ == "__main__":
    main()
