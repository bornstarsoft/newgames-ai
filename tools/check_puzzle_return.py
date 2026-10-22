#!/usr/bin/env python3
"""Check the return-note guide, its boundaries and existing discovery paths."""
from pathlib import Path
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
    assert "the-return-checklist" in page.ids
    assert not Notices(html).notes, "New publication must not be labeled as an update"
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
    assert "#the-return-checklist" in nav.contents_links
    for parent in ("index.html", "blog/index.html", "updates/index.html", "web-games/index.html", "blog/browser-game-save-progress-checklist/index.html"):
        assert route in Page(public / parent).links, parent
    assert page.canonical in {n.text for n in ET.parse(public / "sitemap.xml").iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    for feed in ("blog/index.xml", "updates/index.xml"):
        matches = [n for n in ET.parse(public / feed).findall("./channel/item") if n.findtext("link") == page.canonical]
        assert len(matches) == 1, feed
        if feed.startswith("updates"):
            assert matches[0].findtext("title").startswith("New: ")
    assert all(s.get("type") == "application/ld+json" for s in page.scripts)
    assert "css/guides.css" in html
    print("PASS: published return-note guide, original scope boundaries, six helpful links, five discovery surfaces, closed TOC, canonical/sitemap/both feeds and no fabricated update")


if __name__ == "__main__":
    main()
