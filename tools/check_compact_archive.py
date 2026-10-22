#!/usr/bin/env python3
"""Check that the compact archive retains complete, navigable article records."""
from datetime import datetime
from html.parser import HTMLParser
from pathlib import Path
import re
import sys

from check_updates import Page
from check_visible_updates import Notices


class Archive(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.rows = []
        self.row = self.capture = None
        self.in_list = False
        self.text = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "ul" and attrs.get("class") == "guide-archive-list":
            assert attrs.get("role") == "list"
            self.in_list = True
        if tag == "li" and self.in_list:
            assert self.row is None
            self.row = {"links": [], "images": [], "dates": [], "title": "", "description": "", "meta": ""}
        if self.row is not None:
            if tag == "a": self.row["links"].append(attrs["href"])
            if tag == "img": self.row["images"].append(attrs)
            if tag == "time": self.row["dates"].append(attrs["datetime"])
            if tag == "h3": self.capture = "title"
            if tag == "p": self.capture = "meta" if attrs.get("class") == "guide-archive-meta" else "description"

    def handle_data(self, data):
        self.text.append(data)
        if self.row is not None and self.capture: self.row[self.capture] += data

    def handle_endtag(self, tag):
        if tag in ("h3", "p"): self.capture = None
        if tag == "li" and self.row is not None:
            self.rows.append(self.row)
            self.row = None
        if tag == "ul": self.in_list = False


class Article(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.title = self.description = self.published = ""
        self.in_heading = False
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1": self.in_heading = True
        if tag == "meta" and attrs.get("name") == "description": self.description = attrs["content"]
        if tag == "meta" and attrs.get("property") == "article:published_time": self.published = attrs["content"]

    def handle_data(self, data):
        if self.in_heading: self.title += data

    def handle_endtag(self, tag):
        if tag == "h1": self.in_heading = False


def main():
    root = Path(__file__).resolve().parent.parent
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "public"
    archive = Archive((public / "blog/index.html").read_text())
    published = {"/blog/" + p.parent.name + "/": p for p in (public / "blog").glob("*/index.html")}
    routes, dates = [], []
    assert f"{len(published)} articles." in " ".join(archive.text)
    for row in archive.rows:
        assert len(row["links"]) == 1, "One keyboard stop per article"
        route = row["links"][0]
        assert route in published
        article = Article(published[route].read_text())
        assert row["title"] == article.title
        assert row["description"] == article.description
        notices = Notices(published[route].read_text())
        assert row["dates"] == [article.published[:10]] + notices.dates
        assert re.search(r"\b[1-9][0-9]* min read$", row["meta"])
        assert len(row["images"]) == 1
        image = row["images"][0]
        assert "alt" in image and image["alt"] in (None, "")
        assert {k: image.get(k) for k in ("width", "height", "loading")} == {
            "width": "96", "height": "54", "loading": "lazy"}
        assert (public / image["src"].lstrip("/")).is_file()
        routes.append(route)
        dates.append(datetime.fromisoformat(article.published))
    assert len(routes) == len(set(routes)) and set(routes) == set(published)
    assert dates == sorted(dates, reverse=True)
    for path in public.rglob("*.html"):
        if path == public / "blog/index.html": continue
        assert not Archive(path.read_text()).rows, path
    page = Page(public / "blog/index.html")
    assert page.canonical == "https://newgames.ai/blog/"
    assert {"all-guides", "choose", "learn", "return"} <= page.ids
    print(f"PASS: {len(routes)} unique complete article records, newest-first dates, one title link each, reserved images, reading-time labels, scope and stable fragments")


if __name__ == "__main__":
    main()
