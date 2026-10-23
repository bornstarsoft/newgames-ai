#!/usr/bin/env python3
"""Verify opt-in canonical source lines; browser/PDF checks test print layout."""
from html.parser import HTMLParser
from pathlib import Path
import sys

from check_guide_feedback import TARGETS
from check_updates import Page


class PrintSource(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.inside = False
        self.count = 0
        self.links, self.text = [], []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "p" and attrs.get("class") == "guide-print-source":
            self.count += 1
            self.inside = True
            assert "hidden" not in attrs and "aria-hidden" not in attrs
        if self.inside and tag == "a":
            assert "target" not in attrs
            self.links.append(attrs["href"])

    def handle_data(self, text):
        if self.inside:
            self.text.append(text)

    def handle_endtag(self, tag):
        if tag == "p":
            self.inside = False


def main():
    root = Path(__file__).resolve().parent.parent
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "public"
    expected = {f"blog/{slug}/index.html" for slug in TARGETS} | {"puzzle-terms/index.html"}
    found = set()
    for path in public.rglob("*.html"):
        source = PrintSource(path)
        if not source.count:
            continue
        found.add(path.relative_to(public).as_posix())
        page = Page(path)
        assert source.count == 1 and source.links == [page.canonical]
        assert page.canonical.startswith("https://newgames.ai/")
        assert "".join(source.text) == "NewGames.ai \u00b7 " + page.canonical
        assert "css/guides.css" in path.read_text()
        assert all(s.get("type") == "application/ld+json" for s in page.scripts)
    assert found == expected, (found, expected)
    css = (public / "css/guides.css").read_text()
    assert ".guide-print-source { display: none; }" in css
    assert "@media print" in css and "@page guide" in css
    assert "body:has(.guide-print-source) details:not([open])" in css
    assert "body:has(.guide-print-source) .block-board .block-filled { color: black; background: white; }" in css
    print("PASS: seven opt-in canonical print sources, screen-hidden default, closed-answer print rule, ink-safe block symbols, no script or unrelated page opt-in")


if __name__ == "__main__":
    main()
