#!/usr/bin/env python3
"""Check the reference page and its opt-in learning-guide entry points."""
from html.parser import HTMLParser
from pathlib import Path
import sys
import xml.etree.ElementTree as ET

from check_guide_feedback import TARGETS
from check_guide_finder import GuidePage
from check_updates import Page


ROUTE = "/puzzle-terms/"
TERMS = {
    "cell-row-column-and-box",
    "candidate",
    "one-candidate-in-a-cell",
    "one-place-for-a-digit",
    "contradiction",
    "piece-footprint",
    "line-clear",
    "usable-space",
    "return-note",
}
EXAMPLES = {
    "/blog/how-to-find-your-first-sudoku-move/#start-with-the-three-checks",
    "/blog/how-to-find-your-first-sudoku-move/#check-cross-check",
    "/blog/how-to-find-your-first-sudoku-move/#check-one-left",
    "/blog/sudoku-one-place-for-a-number/#compare-two-row-snapshots",
    "/blog/how-to-find-your-first-sudoku-move/#when-no-candidates-remain",
    "/blog/block-puzzle-fit-clear-leave-space/#check-fit",
    "/blog/block-puzzle-fit-clear-leave-space/#check-clear",
    "/blog/block-puzzle-fit-clear-leave-space/#check-space",
    "/blog/return-to-a-puzzle-after-a-break/#the-return-checklist",
}


class Reference(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.headings, self.social, self.text = set(), {}, []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h2":
            self.headings.add(attrs["id"])
        if tag == "meta" and "property" in attrs:
            self.social[attrs["property"]] = attrs["content"]
        assert tag not in {"form", "input", "iframe"}

    def handle_data(self, text):
        self.text.append(text)


def main():
    root = Path(__file__).resolve().parent.parent
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "public"
    path = public / "puzzle-terms/index.html"
    page, nav, reference = Page(path), GuidePage(path), Reference(path)
    assert page.canonical == "https://newgames.ai" + ROUTE
    assert page.meta["robots"] == "index,follow"
    assert reference.social["og:url"] == page.canonical
    assert reference.social["og:image"].endswith("/images/categories/puzzle-games.svg")
    assert reference.headings == TERMS
    assert nav.disclosures == 1
    assert {href[1:] for href in nav.contents_links if href.startswith("#")} == TERMS
    assert ROUTE not in nav.contents_links, "Do not link the reference to itself"
    assert EXAMPLES <= set(page.links)
    assert page.times == ["2026-10-23"], "Keep the reference's actual publication date"
    assert "css/guides.css" in path.read_text()
    text = " ".join(" ".join(reference.text).replace("\u2019", "'").split())
    for boundary in (
        "not every game's rules or controls",
        "not a confirmed entry",
        "incomplete notes is not enough evidence",
        "it does not save or restore a game's board",
    ):
        assert boundary in text, boundary
    entries = set()
    for html in public.rglob("*.html"):
        links = GuidePage(html).contents_links
        if ROUTE in links:
            assert links.count(ROUTE) == 1
            assert "/blog/" in links
            entries.add(html.relative_to(public).as_posix())
    assert entries == {f"blog/{slug}/index.html" for slug in TARGETS}
    assert ROUTE not in Page(public / "index.html").links
    sitemap = ET.parse(public / "sitemap.xml")
    assert page.canonical in {e.text for e in sitemap.iter("{http://www.sitemaps.org/schemas/sitemap/0.9}loc")}
    for feed in ("blog/index.xml", "updates/index.xml"):
        assert page.canonical not in {e.text for e in ET.parse(public / feed).findall("./channel/item/link")}
    root_items = [e for e in ET.parse(public / "index.xml").findall("./channel/item") if e.findtext("link") == page.canonical]
    assert len(root_items) == 1 and "2026" in root_items[0].findtext("pubDate")
    print("PASS: nine reference terms, nine practice destinations, six guide entry links, closed TOC, canonical/OG/robots/sitemap, no self-link, real root-feed date and no blog/update feed event")


if __name__ == "__main__":
    main()
