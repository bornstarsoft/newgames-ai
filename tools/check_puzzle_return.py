#!/usr/bin/env python3
"""Check the return-note guide, its boundaries and existing discovery paths."""
from pathlib import Path
from email.utils import parsedate_to_datetime
import sys
import xml.etree.ElementTree as ET

from check_updates import Page
from check_guide_finder import GuidePage
from check_visible_updates import Notices


def main():
    root = Path(__file__).resolve().parent.parent
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "public"
    route = "/blog/return-to-a-puzzle-after-a-break/"
    path = public / route.lstrip("/") / "index.html"
    page = Page(path)
    html = path.read_text()
    assert page.canonical == "https://newgames.ai" + route
    assert page.meta["robots"] == "index,follow"
    assert "2026-10-23" in page.times
    assert {"the-return-checklist", "puzzle-note-template", "an-example-of-a-useful-note"} <= page.ids
    assert "#puzzle-note-template" in page.links
    notice = Notices(html)
    assert notice.dates == ["2026-11-10"] and len(notice.notes) == 1
    for text in ("What I checked and what it established", "The choice or question I left open", "One check I can repeat when I return", "one matching detail is not proof", "Do not erase the digit to make the board match the note"):
        assert text in html, text
    for boundary in ("A note does not save a game", "NewGames.ai does not collect or store these notes", "fictional note", "not a supplied board", "Do not reload a valued attempt", "not a backup"):
        if boundary == "not a backup":
            assert boundary in (public / "blog/browser-game-save-progress-checklist/index.html").read_text()
        else:
            assert boundary in html, boundary
    related = [
        "/blog/browser-game-save-progress-checklist/",
        "/blog/how-to-find-your-first-sudoku-move/",
        "/blog/block-puzzle-fit-clear-leave-space/",
        "/blog/number-block-or-color-puzzles-for-your-break/",
        "/puzzle-games/", "/updates/#handy-guides",
    ]
    assert set(related) <= set(page.links)
    nav = GuidePage(path)
    assert nav.disclosures == 1
    assert {"#the-return-checklist", "#puzzle-note-template"} <= set(nav.contents_links)
    for parent in ("index.html", "blog/index.html", "updates/index.html", "web-games/index.html", "blog/browser-game-save-progress-checklist/index.html"):
        assert route in Page(public / parent).links, parent
    assert page.canonical in {n.text for n in ET.parse(public / "sitemap.xml").iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    def feed_items(feed):
        return [n for n in ET.parse(public / feed).findall("./channel/item") if n.findtext("link") == page.canonical]

    original = feed_items("blog/index.xml")
    assert len(original) == 1
    assert parsedate_to_datetime(original[0].findtext("pubDate")).isoformat() == "2026-10-23T02:59:05+09:00"
    events = feed_items("updates/index.xml")
    assert len(events) == 2
    assert [item.findtext("title").split(": ", 1)[0] for item in events] == ["Updated", "New"]
    assert parsedate_to_datetime(events[0].findtext("pubDate")).date().isoformat() == "2026-11-10"
    assert events[1].findtext("pubDate") == original[0].findtext("pubDate")
    assert "reusable puzzle-note template" in events[0].findtext("description")
    assert all(s.get("type") == "application/ld+json" for s in page.scripts)
    assert "css/guides.css" in html
    print("PASS: return-note template and changed-board caution, preserved discovery and publication date, closed TOC, canonical/sitemap and one substantive update event")


if __name__ == "__main__":
    main()
