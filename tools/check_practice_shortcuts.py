#!/usr/bin/env python3
"""Validate opt-in, native practice links without changing article identity."""
from html.parser import HTMLParser
from pathlib import Path
import sys

from check_updates import Page

TARGETS = {
    "how-to-find-your-first-sudoku-move": [
        ("#try-three-small-checks", "Practice examples"),
        ("#start-with-the-three-checks", "Review the steps"),
    ],
    "block-puzzle-fit-clear-leave-space": [
        ("#the-rules-for-these-examples", "Rules & practice"),
        ("#a-small-checklist-for-your-next-session", "Review the steps"),
    ],
}


class Shortcuts(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.in_header = self.in_nav = False
        self.seen_h1 = False
        self.nav_count = 0
        self.links = []
        self.link = None
        self.open_details = 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "header" and attrs.get("class") == "article-hero": self.in_header = True
        if tag == "h1": self.seen_h1 = True
        if tag == "nav" and attrs.get("class") == "guide-shortcuts":
            assert self.in_header and not self.seen_h1
            assert attrs.get("aria-label") == "Practice shortcuts"
            self.nav_count += 1
            self.in_nav = True
        if tag == "a" and self.in_nav:
            assert attrs.get("href", "").startswith("#")
            self.link = [attrs["href"], ""]
        if tag == "details" and "open" in attrs: self.open_details += 1

    def handle_data(self, text):
        if self.link is not None: self.link[1] += text

    def handle_endtag(self, tag):
        if tag == "header": self.in_header = False
        if tag == "nav": self.in_nav = False
        if tag == "a" and self.link is not None:
            self.links.append(tuple(self.link))
            self.link = None


def main():
    root = Path(__file__).resolve().parent.parent
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "public"
    enabled = set()
    for path in public.rglob("*.html"):
        nav = Shortcuts(path)
        if not nav.nav_count: continue
        slug = path.parent.name
        enabled.add(slug)
        assert slug in TARGETS, path
        page = Page(path)
        assert nav.nav_count == 1 and nav.links == TARGETS[slug]
        assert not nav.open_details
        assert all(href[1:] in page.ids for href, _ in nav.links)
        assert page.canonical == f"https://newgames.ai/blog/{slug}/"
        assert page.meta["robots"] == "index,follow" and "2026-10-23" in page.times
        assert all(s.get("type") == "application/ld+json" for s in page.scripts)
        assert "css/guides.css" in path.read_text()
    assert enabled == set(TARGETS)
    print("PASS: two opt-in articles, four native links before titles, valid fragments, closed answers, original dates/canonicals and no executable JS")


if __name__ == "__main__":
    main()
