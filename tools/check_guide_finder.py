#!/usr/bin/env python3
"""Verify complete guide discovery and opt-in table-of-contents links."""
import csv
from datetime import datetime, timezone
from html.parser import HTMLParser
import io
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit

from check_updates import Page


class GuidePage(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.archive = False
        self.archive_links = set()
        self.nav_depth = 0
        self.contents_links = []
        self.disclosures = 0
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and attrs.get("id") == "all-guides":
            self.archive = True
        if tag == "nav":
            if attrs.get("class") == "guide-navigation":
                self.nav_depth = 1
            elif self.nav_depth:
                self.nav_depth += 1
        if tag == "details" and self.nav_depth:
            assert "open" not in attrs
            self.disclosures += 1
        if tag == "a":
            href = attrs.get("href", "")
            if self.archive:
                self.archive_links.add(href)
            if self.nav_depth:
                self.contents_links.append(href)

    def handle_endtag(self, tag):
        if tag == "section":
            self.archive = False
        if tag == "nav" and self.nav_depth:
            self.nav_depth -= 1


def main():
    root = Path(__file__).resolve().parent.parent
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "public"
    inventory = csv.DictReader(io.StringIO(subprocess.check_output(
        ["hugo", "list", "all", "--source", str(root)], text=True)))
    now = datetime.now(timezone.utc)
    published = set()
    for item in inventory:
        if item["section"] != "blog" or item["kind"] != "page":
            continue
        publish = datetime.fromisoformat(item["publishDate"].replace("Z", "+00:00"))
        expiry = datetime.fromisoformat(item["expiryDate"].replace("Z", "+00:00"))
        if item["draft"] == "false" and publish <= now and (expiry.year == 1 or expiry > now):
            published.add(urlsplit(item["permalink"]).path)
    index = public / "blog/index.html"
    page = Page(index)
    assert page.canonical == "https://newgames.ai/blog/"
    assert {"choose", "learn", "return", "all-guides"} <= page.ids
    assert GuidePage(index).archive_links == published, "Archive must retain every published article and no unpublished links"
    assert "/updates/" in page.links
    targets = {
        "browser-game-save-progress-checklist": "2026-10-23",
        "how-to-find-your-first-sudoku-move": "2026-10-23",
        "number-block-or-color-puzzles-for-your-break": "2026-10-14",
    }
    for slug, date in targets.items():
        path = public / "blog" / slug / "index.html"
        article, nav = Page(path), GuidePage(path)
        assert nav.disclosures == 1
        anchors = [href[1:] for href in nav.contents_links if href.startswith("#")]
        assert len(anchors) >= 4 and len(anchors) == len(set(anchors))
        assert set(anchors) <= article.ids
        assert "/blog/" in nav.contents_links
        assert date in article.times
        assert "css/guides.css" in path.read_text()
    for path in (public / "index.html", public / "blog/daysudoku-free-daily-sudoku-game-online/index.html"):
        assert GuidePage(path).disclosures == 0
        assert "css/guides.css" not in path.read_text()
    print(f"PASS: {len(published)} published articles retained; three purpose anchors; three closed TOCs with valid targets; original dates and homepage scope preserved")


if __name__ == "__main__":
    main()
