#!/usr/bin/env python3
"""Check the Ringzzle explanation, discovery links and honest update metadata."""
from html.parser import HTMLParser
from email.utils import parsedate_to_datetime
from pathlib import Path
import xml.etree.ElementTree as ET

from check_updates import Page


class Sections(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.section = None
        self.sections = {}
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in ("h2", "h3"):
            self.section = attrs.get("id")
            self.sections[self.section] = []

    def handle_data(self, text):
        if self.section:
            self.sections[self.section].append(text)

    def text(self, section):
        return " ".join(" ".join(self.sections[section]).split())


def main():
    public = Path(__file__).resolve().parent.parent / "public"
    route = "/blog/ringzzle-free-color-rings-puzzle-game-online/"
    url = "https://newgames.ai" + route
    path = public / route.lstrip("/") / "index.html"
    page, sections = Page(path), Sections(path.read_text())
    assert page.canonical == url and page.meta["robots"] == "index,follow"
    assert "2026-06-09" in page.times and "2026-10-24" in page.times
    assert {"what-ringzzle-is", "no-install-browser-play", "core-rules-and-color-line-clears", "color-burst", "sound-toggle-and-mobile-friendly-play", "anonymous-leaderboard", "before-ending-a-session", "where-to-start", "closing-note"} <= page.ids
    assert {"before-placing-a-ring", "three-small-checks"} <= page.ids
    for key in ("Size:", "Color:", "Space:"):
        assert key in sections.text("before-placing-a-ring")
    assert "small slot is occupied" in sections.text("check-1-a-matching-color-is-not-an-empty-slot")
    assert "small blue ring stays in the right cell" in sections.text("check-2-different-sizes-can-complete-a-line")
    assert "three red rings disappear" in sections.text("check-2-different-sizes-can-complete-a-line")
    assert "distant blue ring clears too; the red ring stays" in sections.text("check-3-a-burst-reaches-beyond-one-line")
    assert "original text examples" in sections.text("three-small-checks")
    assert "Assume no other clear is completed" in sections.text("three-small-checks")
    assert "October 24, 2026" in sections.text("check-3-a-burst-reaches-beyond-one-line")
    assert "not a claim about what Ringzzle saves" in sections.text("before-ending-a-session")
    for href in ("https://ringzzle.com/play/", "https://ringzzle.com/how-to-play/", "https://ringzzle.com/leaderboard/", "/blog/#learn", "/blog/number-block-or-color-puzzles-for-your-break/"):
        assert href in page.links, href
    assert all(s.get("type") == "application/ld+json" for s in page.scripts)
    archive = public / "blog/index.html"
    assert route in Page(archive).links
    assert "Read a Ringzzle move: size, color, space" in archive.read_text()
    items = ET.parse(public / "blog/index.xml").findall("./channel/item")
    assert len(items) == 20
    legacy = [item for item in items if item.findtext("link") == url]
    assert len(legacy) == 1 and "09 Jun 2026" in legacy[0].findtext("pubDate")
    events = ET.parse(public / "updates/index.xml").findall("./channel/item")
    updates = [item for item in events if item.findtext("link") == url and item.findtext("title").startswith("Updated:")]
    assert len(updates) == 1
    assert parsedate_to_datetime(updates[0].findtext("pubDate")).isoformat() == "2026-10-24T02:33:07+09:00"
    assert "Originally published June 9, 2026." in updates[0].findtext("description")
    assert "three examples" in updates[0].findtext("description")
    assert url in {n.text for n in ET.parse(public / "sitemap.xml").iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    print("PASS: three scoped text examples, original anchors/date, official links, Learn entry, one truthful update event and twenty legacy articles; no game-engine test claimed")


if __name__ == "__main__":
    main()
