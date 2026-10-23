#!/usr/bin/env python3
"""Validate truthful visible update notices and their exclusion rules."""
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile


class Notices(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.active = None
        self.dates, self.compact_dates, self.notes = [], [], []
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        classes = attrs.get("class", "").split()
        if tag == "p" and "article-update" in classes:
            self.active = "full"
            self.notes.append("")
        if tag == "span" and "article-update-date" in classes:
            self.active = "compact"
        if tag == "time" and self.active:
            target = self.dates if self.active == "full" else self.compact_dates
            target.append(attrs["datetime"])

    def handle_data(self, text):
        if self.active == "full":
            self.notes[-1] += text

    def handle_endtag(self, tag):
        if (tag == "p" and self.active == "full") or (tag == "span" and self.active == "compact"):
            self.active = None


def fixtures(root):
    parent = root / "output/playwright"
    parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="notice-fixtures-", dir=parent) as folder:
        site = Path(folder)
        (site / "layouts/partials").mkdir(parents=True)
        (site / "layouts/_default").mkdir()
        (site / "content/blog").mkdir(parents=True)
        shutil.copyfile(root / "layouts/partials/article-update.html", site / "layouts/partials/article-update.html")
        (site / "hugo.toml").write_text('baseURL = "https://example.invalid/"\n')
        (site / "layouts/_default/single.html").write_text(
            '<main>{{ .Title }}{{ partial "article-update.html" (dict "page" . "compact" false) }}'
            '{{ partial "article-update.html" (dict "page" . "compact" true) }}</main>')
        cases = {
            "updated": {},
            "missing-note": {"updateNote": ""},
            "blank-note": {"updateNote": "  \n "},
            "same-date": {"lastmod": "2020-01-01"},
            "earlier-date": {"lastmod": "2019-12-31"},
            "future-update": {"lastmod": "2999-01-02"},
            "future-post": {"publishDate": "2999-01-01", "lastmod": "2999-01-02"},
            "delayed": {"publishDate": "2020-03-01", "lastmod": "2020-02-01"},
            "draft": {"draft": True},
            "expired": {"expiryDate": "2020-01-03"},
        }
        note = '  Checked <b> & "quotes" safely.  '
        for name, changes in cases.items():
            data = dict(title=name, date="2020-01-01", lastmod="2020-01-02", updateNote=note)
            data.update(changes)
            (site / f"content/blog/{name}.md").write_text(json.dumps(data))
        (site / "content/about.md").write_text(json.dumps(dict(title="About", date="2020-01-01", lastmod="2020-01-02", updateNote=note)))
        subprocess.run(["hugo", "--source", str(site), "--buildDrafts", "--buildFuture", "--buildExpired"], check=True, capture_output=True)
        for name in cases:
            html = (site / f"public/blog/{name}/index.html").read_text()
            parsed = Notices(html)
            if name == "updated":
                assert parsed.dates == parsed.compact_dates == ["2020-01-02"]
                assert parsed.notes == ['Updated January 2, 2020: Checked <b> & "quotes" safely.']
                assert "<b>" not in html and "&lt;b&gt;" in html
            else:
                assert not parsed.dates and not parsed.compact_dates and not parsed.notes, name
        assert not Notices((site / "public/about/index.html").read_text()).notes
    print("PASS fixtures: explicit meaningful dates, escaped note, whitespace, same/earlier/future dates, delayed publication, preview drafts, expiry and non-blog exclusions")


def main():
    root = Path(__file__).resolve().parent.parent
    public = root / "public"
    expected = {
        "daysudoku-free-daily-sudoku-game-online": ("2026-10-14", "Revised the introduction to reflect the current classic daily Sudoku format and linked the official rules."),
        "how-to-find-your-first-sudoku-move": ("2026-10-23", "Added a worked example for an empty candidate set and a cautious rechecking routine."),
        "block-puzzle-fit-clear-leave-space": ("2026-10-23", "Added result boards to compare the space left after each legal placement and line clear."),
    }
    found = set()
    for path in public.rglob("*.html"):
        notice = Notices(path.read_text())
        if path == public / "blog/index.html":
            assert sorted(notice.compact_dates) == sorted(x[0] for x in expected.values())
            assert not notice.notes
            continue
        assert not notice.compact_dates
        if notice.notes:
            slug = path.parent.name
            assert slug in expected, path
            date, note = expected[slug]
            assert notice.dates == [date] and len(notice.notes) == 1
            assert notice.notes[0].endswith(": " + note)
            found.add(slug)
    assert found == set(expected)
    print(f"PASS: only {len(expected)} substantively updated articles have dated notes and matching archive labels")
    fixtures(root)


if __name__ == "__main__":
    main()
