#!/usr/bin/env python3
"""Check the static error page without changing published page indexing."""
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import urlsplit
import xml.etree.ElementTree as ET

from check_updates import Page


class Recovery(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.inside = False
        self.count = 0
        self.links = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "nav" and attrs.get("aria-label") == "Find another page":
            self.inside = True
            self.count += 1
        if self.inside and tag == "a":
            assert "target" not in attrs
            self.links.append(attrs["href"])
        assert tag != "meta" or attrs.get("http-equiv", "").lower() != "refresh"

    def handle_endtag(self, tag):
        if tag == "nav":
            self.inside = False


def main():
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("public")
    error = public / "404.html"
    page = Page(error)
    recovery = Recovery(error.read_text())
    assert page.meta["robots"] == "noindex,follow"
    assert recovery.count == 1
    assert recovery.links == ["/blog/", "/blog/#learn", "/updates/"]
    assert "/" in page.links and "/contact/" in page.links
    assert not page.scripts
    for link in recovery.links + ["/", "/contact/"]:
        url = urlsplit(link)
        target = Page(public / url.path.lstrip("/") / "index.html")
        assert target.meta["robots"] == "index,follow", link
        if url.fragment:
            assert url.fragment in target.ids, link
    sitemap = {n.text for n in ET.parse(public / "sitemap.xml").iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    assert "https://newgames.ai/404.html" not in sitemap
    for url in sitemap:
        route = urlsplit(url).path
        target = public / route.lstrip("/") / "index.html"
        assert Page(target).meta["robots"] == "index,follow", route
    assert not any("_draft-template" in p.name for p in public.rglob("*"))
    print("PASS: noindex 404, three working recovery paths, home/contact links, no redirect/script, unchanged sitemap page indexing and draft exclusion")


if __name__ == "__main__":
    main()
