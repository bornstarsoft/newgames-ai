#!/usr/bin/env python3
"""Check combined RSS semantics and isolated Hugo regression fixtures."""
import argparse
from datetime import datetime, timedelta, timezone
from email.utils import parsedate_to_datetime
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET

from check_updates import Page

BASE = "https://newgames.ai"
ATOM = "{http://www.w3.org/2005/Atom}"


def inspect_feed(path):
    rss = ET.parse(path).getroot()
    assert rss.tag == "rss" and rss.get("version") == "2.0"
    channel = rss.find("channel")
    assert channel.findtext("title") == "NewGames.ai - New & Updated"
    assert channel.findtext("link") == BASE + "/updates/"
    assert channel.findtext("description") and channel.findtext("language") == "en-us"
    reference = channel.find(ATOM + "link")
    assert reference.attrib == {"href": BASE + "/updates/index.xml", "rel": "self", "type": "application/rss+xml"}
    items = channel.findall("item")
    assert len(items) <= 20
    dates, identifiers = [], []
    for item in items:
        title, link, guid = item.findtext("title"), item.findtext("link"), item.find("guid")
        kind, separator, _ = title.partition(": ")
        assert separator and kind in ("New", "Updated")
        assert link.startswith(BASE + "/blog/") and link.endswith("/")
        date = parsedate_to_datetime(item.findtext("pubDate"))
        assert date.tzinfo and date <= datetime.now(timezone.utc)
        dates.append(date)
        stamp = date.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        assert guid.get("isPermaLink") == "false"
        assert guid.text == f"{link}#{kind.lower()}-{stamp}"
        identifiers.append(guid.text)
        assert item.findtext("description")
    assert dates == sorted(dates, reverse=True)
    assert len(set(identifiers)) == len(identifiers)
    if items:
        assert parsedate_to_datetime(channel.findtext("lastBuildDate")) == dates[0]
    else:
        assert channel.find("lastBuildDate") is None
    return items


class FeedReference(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.urls = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "link" and attrs.get("rel") == "alternate" and attrs.get("type") == "application/rss+xml":
            self.urls.append(attrs.get("href"))


def check_public(public):
    items = inspect_feed(public / "updates/index.xml")
    new = {i.findtext("link"): i for i in items if i.findtext("title").startswith("New: ")}
    legacy = ET.parse(public / "blog/index.xml").findall("./channel/item")
    # Today's entire 18-article catalogue fits. For larger feeds check retained events.
    if len(items) < 20:
        assert set(new) == {i.findtext("link") for i in legacy}
    for old in legacy:
        if old.findtext("link") in new:
            current = new[old.findtext("link")]
            assert current.findtext("title") == "New: " + old.findtext("title")
            assert parsedate_to_datetime(current.findtext("pubDate")) == parsedate_to_datetime(old.findtext("pubDate"))
    corrections = [i for i in items if i.findtext("title").startswith("Updated: ")]
    day = next(i for i in corrections if i.findtext("link") == BASE + "/blog/daysudoku-free-daily-sudoku-game-online/")
    assert parsedate_to_datetime(day.findtext("pubDate")).date().isoformat() == "2026-10-14"
    assert "Originally published June 15, 2026." in day.findtext("description")
    assert "classic daily Sudoku format" in day.findtext("description")
    page = Page(public / "updates/index.html")
    assert {"/updates/index.xml", "/blog/index.xml"} <= set(page.links)
    assert FeedReference(public / "updates/index.html").urls == [BASE + "/updates/index.xml"]
    assert FeedReference(public / "blog/index.html").urls == [BASE + "/blog/index.xml"]
    for item in items:
        assert (public / item.findtext("link").removeprefix(BASE).lstrip("/") / "index.html").is_file()
    print(f"PASS: {len(items)} feed events, valid XML/dates/IDs, existing correction, legacy feed compatibility, visible links and RSS autodiscovery")


def fixtures(root):
    parent = root / "output/playwright"
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="rss-fixture-", dir=parent) as folder:
        site = Path(folder)
        for directory in ("layouts/updates", "layouts/_default", "content/updates", "content/blog"):
            (site / directory).mkdir(parents=True)
        shutil.copyfile(root / "hugo.toml", site / "hugo.toml")
        shutil.copyfile(root / "layouts/updates/rss.xml", site / "layouts/updates/rss.xml")
        for name in ("single", "list"):
            (site / f"layouts/_default/{name}.html").write_text("<main>{{ .Title }}</main>")
        (site / "content/updates/_index.md").write_text(json.dumps({"title": "New & Updated", "outputs": ["HTML", "RSS"]}))

        def post(slug, **changes):
            data = {"title": 'A & B "quoted" <test>', "slug": slug,
                    "description": "A reader's check & another choice.", "date": "2020-01-01T00:00:00Z", "draft": False}
            data.update(changes)
            (site / f"content/blog/{slug}.md").write_text(json.dumps(data) + "\n\nFixture only.")

        def build(inclusive=False):
            command = ["hugo", "--source", str(site), "--minify", "--cleanDestinationDir"]
            if inclusive: command += ["--buildDrafts", "--buildFuture", "--buildExpired"]
            result = subprocess.run(command, text=True, capture_output=True, timeout=60)
            assert result.returncode == 0, result.stdout + result.stderr
            path = site / "public/updates/index.xml"
            return inspect_feed(path), path.read_bytes()

        post("plain")
        post("corrected", lastmod="2020-01-05T00:00:00Z", updateNote="Corrected A & B; <em>keep checking</em>.")
        post("future-note", lastmod="2099-01-01T00:00:00Z", updateNote="Not yet.")
        post("blank-note", lastmod="2020-01-05T00:00:00Z", updateNote="  \n ")
        post("no-note", lastmod="2020-01-05T00:00:00Z")
        post("same-date", lastmod="2020-01-01T00:00:00Z", updateNote="Not later.")
        post("early-note", lastmod="2019-01-01T00:00:00Z", updateNote="Before publication.")
        post("delayed", publishDate="2020-03-01T00:00:00Z", lastmod="2020-02-01T00:00:00Z", updateNote="Still before publication.")
        post("draft", draft=True, lastmod="2020-01-05T00:00:00Z", updateNote="Excluded.")
        post("scheduled", publishDate="2099-01-01T00:00:00Z")
        post("expired", expiryDate="2021-01-01T00:00:00Z")
        items, initial = build()
        assert len(items) == 9
        assert sum(i.findtext("title").startswith("Updated: ") for i in items) == 1
        plain = next(i for i in items if i.findtext("link").endswith("/plain/"))
        assert plain.findtext("title") == 'New: A & B "quoted" <test>'
        assert plain.findtext("description") == "A reader's check & another choice."
        correction = next(i for i in items if i.findtext("title").startswith("Updated: "))
        assert correction.findtext("description") == "Corrected A & B; keep checking. Originally published January 1, 2020."
        assert items[0].findtext("link").endswith("/delayed/")
        assert parsedate_to_datetime(items[0].findtext("pubDate")).date().isoformat() == "2020-03-01"
        assert build()[1] == initial, "Rebuild changed unchanged feed"
        assert build(True)[1] == initial, "Inclusive preview leaked unpublished events"
        for i in range(25):
            post(f"limit-{i}", date=(datetime(2022, 1, 1, tzinfo=timezone.utc) + timedelta(days=i)).isoformat())
        capped, _ = build()
        assert len(capped) == 20 and capped[0].findtext("link").endswith("/limit-24/")
        assert capped[-1].findtext("link").endswith("/limit-5/")
        for path in (site / "content/blog").glob("*.md"): path.unlink()
        assert not build()[0]
    print("PASS fixtures: escaping, delayed publication, one meaningful correction, draft/future/expiry/blank exclusions, stable rebuilds, preview flags, 20-event cap, empty feed")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("public", nargs="?", type=Path)
    parser.add_argument("--fixtures", action="store_true")
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    check_public(args.public or root / "public")
    if args.fixtures: fixtures(root)
