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
        if tag == "link" and attrs.get("rel") == "canonical": self.canonical = attrs.get("href")


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
    assert page.canonical == "https://newgames.ai/updates/"
    assert page.meta["robots"] == "index,follow"
    assert {"new-guides", "updated-guides", "handy-guides"} <= page.ids
    assert "/blog/index.xml" in page.links
    assert "/blog/number-block-or-color-puzzles-for-your-break/" in page.links
    assert "2026-06-15" in page.times and "2026-10-14" in page.times
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
    for path in public.rglob("*.html"):
        p = Page(path)
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
