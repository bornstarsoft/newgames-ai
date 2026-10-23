#!/usr/bin/env python3
"""Verify the worked conflict, stable article identity, and update discovery."""
from html.parser import HTMLParser
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from check_updates import Page

ROUTE = "/blog/how-to-find-your-first-sudoku-move/"
ANCHOR = "when-no-candidates-remain"
NOTE = "Added step-by-step candidate tables to the three practice answers. The earlier conflicting-notes example and rechecking routine remain available."


class Recheck(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.active = False
        self.cell = None
        self.cells = []
        self.text = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        if tag == "h2":
            self.active = dict(attrs).get("id") == ANCHOR
        if self.active and tag in ("th", "td"):
            self.cell = ""

    def handle_data(self, text):
        if self.active:
            self.text.append(text)
        if self.cell is not None:
            self.cell += text

    def handle_endtag(self, tag):
        if tag in ("th", "td") and self.cell is not None:
            self.cells.append(self.cell.strip())
            self.cell = None


def main():
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "public"
    path = public / ROUTE.lstrip("/") / "index.html"
    page = Page(path)
    section = Recheck(path.read_text())
    assert section.cells == [
        "Your written check", "Digits already present",
        "Row", "1, 2, 3, 4, 6, 7, 8, 9", "Column", "5", "Box", "1, 2, 4",
    ]
    groups = [set(map(int, section.cells[i].split(","))) for i in (3, 5, 7)]
    digits = set(range(1, 10))
    assert digits - groups[0] == {5}
    assert not digits.difference(*groups)
    assert digits.difference(groups[0], {2}, groups[2]) == {5}, "A changed column must change the result"
    text = " ".join(section.text)
    for boundary in ("deliberately conflicting notes", "not a valid puzzle", "Do not change an original clue", "rather than clearing the board or guessing"):
        assert boundary in text
    assert ANCHOR in page.ids and "#" + ANCHOR in page.links
    assert {"try-three-small-checks", "start-with-the-three-checks"} <= page.ids
    assert page.canonical == "https://newgames.ai" + ROUTE
    assert page.meta["robots"] == "index,follow"
    assert "2026-10-23" in page.times
    updates = Page(public / "updates/index.html")
    assert ROUTE in updates.links and NOTE in (public / "updates/index.html").read_text()
    items = ET.parse(public / "updates/index.xml").findall("./channel/item")
    matches = [i for i in items if i.findtext("link") == page.canonical and i.findtext("title").startswith("Updated: ")]
    assert len(matches) == 1 and NOTE in matches[0].findtext("description")
    assert matches[0].findtext("guid").endswith("#updated-20261023T122830Z")
    legacy = ET.parse(public / "blog/index.xml").findall("./channel/item")
    assert sum(i.findtext("link") == page.canonical for i in legacy) == 1
    print("PASS: conflicting notes yield no candidate, counter-check yields 5, boundaries, original anchors/canonical, one update event and one legacy feed entry")


if __name__ == "__main__":
    main()
