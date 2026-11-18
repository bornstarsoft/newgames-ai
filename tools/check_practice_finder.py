#!/usr/bin/env python3
"""Check the compact practice finder against the actual rendered exercises."""
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import urlsplit

from check_example_links import Examples
from check_updates import Page


class Finder(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.count = 0
        self.active = False
        self.in_topics = False
        self.capture = None
        self.summary = ""
        self.groups = []
        self.group_ids = []
        self.topics = []
        self.topic_nav_count = 0
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
        if tag == "nav":
            assert attrs.get("aria-label") == "Practice topics" and not self.groups
            self.in_topics = True
            self.topic_nav_count += 1
        if tag == "h3":
            assert attrs.get("tabindex") == "-1"
            self.group_ids.append(attrs["id"])
            self.groups.append("")
            self.capture = "heading"
        if tag == "a":
            assert not ({"onclick", "target", "download"} & attrs.keys())
            collection = self.topics if self.in_topics else self.links
            collection.append([attrs["href"], ""])
            self.capture = "topic" if self.in_topics else "link"

    def handle_data(self, data):
        if self.capture == "summary": self.summary += data
        if self.capture == "heading": self.groups[-1] += data
        if self.capture == "link": self.links[-1][1] += data
        if self.capture == "topic": self.topics[-1][1] += data

    def handle_endtag(self, tag):
        if tag in ("a", "h3", "summary"): self.capture = None
        if tag == "nav": self.in_topics = False
        if tag == "details": self.active = False


def main():
    root = Path(__file__).resolve().parent.parent
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "public"
    index = public / "blog/index.html"
    updates = public / "updates/index.html"
    missing = public / "404.html"
    assert Page(index).links.count("#practice-examples") == 1
    assert Page(updates).links.count("/blog/#practice-examples") == 1
    assert Page(missing).links.count("/blog/#practice-examples") == 1
    finder = Finder(index.read_text())
    assert finder.count == 1
    assert finder.summary == "Choose a practice example"
    assert finder.groups == ["Sudoku: check a cell", "Sudoku: find a place", "Blocks: fit, clear, space", "Rings: size, color, space"]
    assert finder.topic_nav_count == 1
    assert finder.topics == [
        ["#practice-sudoku-basics", "Sudoku basics"], ["#practice-sudoku-next", "Sudoku next steps"],
        ["#practice-blocks", "Blocks"], ["#practice-rings", "Rings"],
    ]
    assert finder.group_ids == [href[1:] for href, _ in finder.topics]
    expected = []
    for slug in ("how-to-find-your-first-sudoku-move", "sudoku-one-place-for-a-number", "block-puzzle-fit-clear-leave-space"):
        route = f"/blog/{slug}/"
        for example in Examples((public / route.lstrip("/") / "index.html").read_text()).items:
            expected.append([route + "#" + example["id"], example["text"]])
        if slug == "sudoku-one-place-for-a-number":
            assert "when-two-places-share-a-row" in Page(public / route.lstrip("/") / "index.html").ids
            expected.append([route + "#when-two-places-share-a-row", "Remove a candidate without placing a digit"])
    assert len(expected) == 10
    ring_path = "/blog/ringzzle-free-color-rings-puzzle-game-online/"
    ring = Page(public / ring_path.lstrip("/") / "index.html")
    for anchor, label in (
        ("check-1-a-matching-color-is-not-an-empty-slot", "Check 1: Find an empty size slot"),
        ("check-2-different-sizes-can-complete-a-line", "Check 2: Complete a line with different sizes"),
        ("check-3-a-burst-reaches-beyond-one-line", "Check 3: See what a Color Burst removes"),
    ):
        assert anchor in ring.ids and f"#{anchor}" in ring.links
        expected.append([ring_path + "#" + anchor, label])
    assert finder.links == expected, "Keep all examples in their article teaching order"
    assert len({href for href, _ in finder.links}) == 13
    for href, _ in finder.links:
        assert urlsplit(href).fragment
    for path in public.rglob("*.html"):
        if path != index: assert Finder(path.read_text()).count == 0, path
        if path not in (updates, missing): assert "/blog/#practice-examples" not in Page(path).links, path
    print("PASS: guide, updates and missing-page entry links, one closed finder, four topic jumps and thirteen ordered examples")


if __name__ == "__main__":
    main()
