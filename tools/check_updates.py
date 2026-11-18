#!/usr/bin/env python3
"""Check the production updates page using the Python standard library."""
from html.parser import HTMLParser
import csv
from datetime import datetime, timezone
import io
from pathlib import Path
import subprocess
import sys
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET


class Page(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.links, self.images, self.scripts, self.times = [], [], [], []
        self.ids, self.meta = set(), {}
        self.canonical = None
        self.has_update_notice = False
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs:
            assert attrs["id"] not in self.ids, "Duplicate ID"
            self.ids.add(attrs["id"])
        if tag == "a": self.links.append(attrs.get("href", ""))
        if tag == "img": self.images.append(attrs)
        if tag == "script": self.scripts.append(attrs)
        if tag == "time": self.times.append(attrs.get("datetime"))
        if tag == "meta": self.meta[attrs.get("name")] = attrs.get("content")
        if tag == "p" and "article-update" in attrs.get("class", "").split():
            self.has_update_notice = True
        if tag == "link" and attrs.get("rel") == "canonical": self.canonical = attrs.get("href")


class UpdateLinks(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.in_updates = False
        self.in_link = False
        self.in_history = False
        self.rows = []
        self.earlier = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section":
            self.in_updates = attrs.get("id") == "updated-guides"
        if self.in_updates and tag == "details":
            assert attrs.get("id") == "earlier-guide-updates" and "open" not in attrs
            self.in_history = True
        rows = self.earlier if self.in_history else self.rows
        if self.in_updates and tag == "li":
            rows.append([])
        if self.in_updates and tag == "a":
            assert "target" not in attrs
            rows[-1].append([attrs["href"], ""])
            self.in_link = True

    def handle_data(self, data):
        if self.in_link:
            rows = self.earlier if self.in_history else self.rows
            rows[-1][-1][1] += data

    def handle_endtag(self, tag):
        if tag == "a":
            self.in_link = False
        if tag == "details":
            self.in_history = False
        if tag == "section":
            self.in_updates = False


def check_update_links(path):
    expected = {
        "/blog/block-puzzle-fit-clear-leave-space/": ("check-tradeoff", "Try the one-line versus two-line exercise"),
        "/blog/how-to-find-web-games-that-fit-short-breaks/": ("when-a-web-game-will-not-load", "Check a game that will not load"),
        "/blog/return-to-a-puzzle-after-a-break/": ("rehearse-a-return-on-a-fixed-board", "Rehearse a return on a fixed board"),
        "/blog/sudoku-one-place-for-a-number/": ("when-two-places-share-a-row", "Try the box-to-row Sudoku check"),
        "/blog/number-block-or-color-puzzles-for-your-break/": ("check-the-board-without-relying-on-color", "Try the color and symbol check"),
        "/blog/ringzzle-free-color-rings-puzzle-game-online/": ("three-small-checks", "Try the three Ringzzle checks"),
    }
    routes = set()
    listing = UpdateLinks(path)
    assert len(listing.rows) == 6, "Keep the latest updates list capped at six"
    for title, *jumps in listing.rows + listing.earlier:
        route = title[0]
        assert not urlsplit(route).fragment
        assert route not in routes
        routes.add(route)
        if route not in expected:
            assert not jumps
            continue
        anchor, label = expected[route]
        assert jumps == [[f"{route}#{anchor}", label]]
    assert set(expected) <= routes
    return {row[0][0] for row in listing.rows}, routes


def main():
    public = (Path(sys.argv[1]) if len(sys.argv) > 1 else Path("public")).resolve()
    source = Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else Path(__file__).resolve().parent.parent
    inventory = csv.DictReader(io.StringIO(subprocess.check_output(
        ["hugo", "list", "all", "--source", str(source)], text=True)))
    now = datetime.now(timezone.utc)
    excluded = []
    for item in inventory:
        if item["kind"] != "page":
            continue
        publish_date = datetime.fromisoformat(item["publishDate"].replace("Z", "+00:00"))
        expiry_date = datetime.fromisoformat(item["expiryDate"].replace("Z", "+00:00"))
        if item["draft"] == "true" or publish_date > now or (expiry_date.year > 1 and expiry_date <= now):
            excluded.append(urlsplit(item["permalink"]).path)
    page = Page(public / "updates/index.html")
    recent_updates, all_updates = check_update_links(public / "updates/index.html")
    assert page.canonical == "https://newgames.ai/updates/"
    assert page.meta["robots"] == "index,follow"
    assert {"new-guides", "updated-guides", "handy-guides"} <= page.ids
    assert "/blog/index.xml" in page.links
    compare_path = "/blog/number-block-or-color-puzzles-for-your-break/"
    assert compare_path in page.links
    compare = Page(public / compare_path.lstrip("/") / "index.html")
    assert compare.canonical == "https://newgames.ai" + compare_path
    assert {"2026-10-14", "2026-11-18"} <= set(compare.times)
    color_check = "check-the-board-without-relying-on-color"
    assert {"try-one-decision-before-choosing", color_check} <= compare.ids
    assert f"#{color_check}" in compare.links
    assert "https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html" in compare.links
    assert compare_path + "#" + color_check in Page(public / "puzzle-games/index.html").links
    assert {
        "/blog/how-to-find-your-first-sudoku-move/#check-one-left",
        "/blog/block-puzzle-fit-clear-leave-space/#check-fit",
        "/blog/ringzzle-free-color-rings-puzzle-game-online/#check-2-different-sizes-can-complete-a-line",
    } <= set(compare.links)
    ring = Page(public / "blog/ringzzle-free-color-rings-puzzle-game-online/index.html")
    assert "check-2-different-sizes-can-complete-a-line" in ring.ids
    day = Page(public / "blog/daysudoku-free-daily-sudoku-game-online/index.html")
    assert {"2026-06-15", "2026-10-14"} <= set(day.times)
    break_path = "/blog/how-to-find-web-games-that-fit-short-breaks/"
    assert break_path in recent_updates
    break_guide = Page(public / break_path.lstrip("/") / "index.html")
    assert break_guide.canonical == "https://newgames.ai" + break_path
    assert {"2026-06-03", "2026-11-18"} <= set(break_guide.times)
    assert {"try-a-five-minute-break-budget", "when-a-web-game-will-not-load"} <= break_guide.ids
    assert "/blog/browser-game-save-progress-checklist/#the-short-checklist" in break_guide.links
    assert "/blog/browser-game-save-progress-checklist/#do-not-clear-site-data-as-a-first-fix" in break_guide.links
    assert "https://support.google.com/chrome/answer/6098869" in break_guide.links
    assert break_path + "#when-a-web-game-will-not-load" in Page(public / "web-games/index.html").links
    mobile_path = "/blog/how-to-choose-a-new-mobile-game-for-quick-sessions/"
    assert mobile_path in recent_updates
    mobile = Page(public / mobile_path.lstrip("/") / "index.html")
    assert mobile.canonical == "https://newgames.ai" + mobile_path
    assert {"2026-06-03", "2026-11-18"} <= set(mobile.times)
    assert "try-three-moves-in-your-usual-setup" in mobile.ids
    sitemap = {n.text for n in ET.parse(public / "sitemap.xml").iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    assert page.canonical in sitemap
    rss = ET.parse(public / "blog/index.xml")
    assert rss.findall("./channel/item")
    save_path = "/blog/browser-game-save-progress-checklist/"
    assert save_path in page.links
    save = Page(public / save_path.lstrip("/") / "index.html")
    assert save.canonical == "https://newgames.ai" + save_path
    assert save.meta["robots"] == "index,follow"
    assert "the-short-checklist" in save.ids
    assert "/updates/#handy-guides" in save.links
    assert save.canonical in sitemap
    assert save.canonical in {n.text for n in rss.findall("./channel/item/link")}
    assert save_path in Page(public / "web-games/index.html").links
    count = 0
    noticed_updates = set()
    for path in public.rglob("*.html"):
        p = Page(path)
        if p.has_update_notice:
            noticed_updates.add(urlsplit(p.canonical).path)
        count += 1
        assert "/updates/" in p.links, (path, "Missing footer updates link")
        assert all(s.get("type") == "application/ld+json" for s in p.scripts), path
        for link in p.links:
            u = urlsplit(link)
            if u.scheme or u.netloc: continue
            target = public / unquote(u.path).lstrip("/") if u.path.startswith("/") else path.parent / unquote(u.path) if u.path else path
            if target.is_dir(): target /= "index.html"
            assert target.exists(), (path, link)
            if u.fragment and target.suffix == ".html":
                assert unquote(u.fragment) in Page(target).ids, (path, link)
        for img in p.images:
            assert img.get("width") and img.get("height") and "alt" in img
            assert (public / img["src"].lstrip("/")).is_file()
    assert all_updates == noticed_updates, "Each article update must be discoverable exactly once"
    for path in public.rglob("*"):
        if path.suffix in (".xml", ".html"):
            markup = path.read_text()
            for route in excluded:
                assert route not in markup, (path, "Unpublished route leaked", route)
    for route in excluded:
        assert not (public / route.lstrip("/")).exists(), route
    print(f"PASS: {count} HTML pages, links/images/anchors, updates and useful guides, save article metadata/sitemap/RSS, no executable JS, {len(excluded)} unpublished routes excluded")


if __name__ == "__main__":
    main()
