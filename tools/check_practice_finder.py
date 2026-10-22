#!/usr/bin/env python3
"""Check the compact practice finder against the actual rendered exercises."""
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import urlsplit

from check_example_links import Examples


class Finder(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.count = 0
        self.active = False
        self.capture = None
        self.summary = ""
        self.groups = []
        self.links = []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "details" and attrs.get("id") == "practice-examples":
            assert attrs.get("class") == "practice-finder"
            assert "open" not in attrs
            self.active = True
            self.count += 1
        if not self.active:
            return
        if tag == "summary": self.capture = "summary"
        if tag == "h3":
            self.groups.append("")
            self.capture = "heading"
        if tag == "a":
            assert not ({"onclick", "target", "download"} & attrs.keys())
            self.links.append([attrs["href"], ""])
            self.capture = "link"

    def handle_data(self, data):
        if self.capture == "summary": self.summary += data
        if self.capture == "heading": self.groups[-1] += data
        if self.capture == "link": self.links[-1][1] += data

    def handle_endtag(self, tag):
        if tag in ("a", "h3", "summary"): self.capture = None
        if tag == "details": self.active = False


def main():
    root = Path(__file__).resolve().parent.parent
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "public"
    index = public / "blog/index.html"
    finder = Finder(index.read_text())
    assert finder.count == 1
    assert finder.summary == "Choose a practice example"
    assert finder.groups == ["Sudoku: check a cell", "Sudoku: find a place", "Blocks: fit, clear, space"]
    expected = []
    for slug in ("how-to-find-your-first-sudoku-move", "sudoku-one-place-for-a-number", "block-puzzle-fit-clear-leave-space"):
        route = f"/blog/{slug}/"
        for example in Examples((public / route.lstrip("/") / "index.html").read_text()).items:
            expected.append([route + "#" + example["id"], example["text"]])
    assert len(expected) == 8 and finder.links == expected, "Keep all examples in their article teaching order"
    assert len({href for href, _ in finder.links}) == 8
    for href, _ in finder.links:
        assert urlsplit(href).fragment
    for path in public.rglob("*.html"):
        if path != index: assert Finder(path.read_text()).count == 0, path
    print("PASS: one closed finder, three skill groups, eight ordered exact example links/labels, native same-tab links, directory-only scope")


if __name__ == "__main__":
    main()
