#!/usr/bin/env python3
"""Validate truthful visible update notices and their exclusion rules."""
from html.parser import HTMLParser
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

from check_practice_shortcuts import Shortcuts
from check_updates import UpdateLinks


class Notices(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.active = None
        self.in_link = False
        self.dates, self.compact_dates, self.notes = [], [], []
        self.links = []
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
        if tag == "a" and self.active:
            assert self.active == "full" and attrs["href"].startswith("#")
            assert not ({"target", "onclick"} & attrs.keys())
            self.links.append([attrs["href"], ""])
            self.in_link = True

    def handle_data(self, text):
        if self.in_link:
            self.links[-1][1] += text
        elif self.active == "full":
            self.notes[-1] += text

    def handle_endtag(self, tag):
        if tag == "a":
            self.in_link = False
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
            "no-link": {"updateLink": None},
            "missing-label": {"updateLink": {"anchor": "changed"}},
            "duplicate-shortcut": {"guideNavigation": True, "guideShortcuts": [{"anchor": "changed"}]},
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
            data = dict(title=name, date="2020-01-01", lastmod="2020-01-02", updateNote=note,
                        updateLink={"anchor": "changed", "label": "Read <the change> & return"})
            data.update(changes)
            (site / f"content/blog/{name}.md").write_text(json.dumps(data) + "\n\n## Changed\n")
        (site / "content/about.md").write_text(json.dumps(dict(title="About", date="2020-01-01", lastmod="2020-01-02", updateNote=note)))
        subprocess.run(["hugo", "--source", str(site), "--buildDrafts", "--buildFuture", "--buildExpired"], check=True, capture_output=True)
        for name in cases:
            html = (site / f"public/blog/{name}/index.html").read_text()
            parsed = Notices(html)
            if name in {"updated", "no-link", "missing-label", "duplicate-shortcut"}:
                assert parsed.dates == parsed.compact_dates == ["2020-01-02"]
                assert [note.strip() for note in parsed.notes] == ['Updated January 2, 2020: Checked <b> & "quotes" safely.']
                assert parsed.links == ([["#changed", "Read <the change> & return"]] if name == "updated" else [])
                assert "<b>" not in html and "&lt;b&gt;" in html
            else:
                assert not parsed.dates and not parsed.compact_dates and not parsed.notes and not parsed.links, name
        assert not Notices((site / "public/about/index.html").read_text()).notes
    print("PASS fixtures: dated notices, escaped text, optional and duplicate links, preview and publication exclusions")


def main():
    root = Path(__file__).resolve().parent.parent
    public = root / "public"
    expected = {
        "daysudoku-free-daily-sudoku-game-online": ("2026-10-14", "Revised the introduction to reflect the current classic daily Sudoku format and linked the official rules."),
        "how-to-find-your-first-sudoku-move": ("2026-10-23", "Added step-by-step candidate tables to the three practice answers. The earlier conflicting-notes example and rechecking routine remain available."),
        "block-puzzle-fit-clear-leave-space": ("2026-11-18", "Added a block exercise where clearing one line leaves room for the next square but clearing two does not."),
        "ringzzle-free-color-rings-puzzle-game-online": ("2026-11-18", "Made all three answers reveal on demand and added a follow-up about which slots open after a clear."),
        "return-to-a-puzzle-after-a-break": ("2026-11-18", "Added a short rehearsal for leaving a puzzle note and using it to resume a fixed block exercise."),
        "sudoku-one-place-for-a-number": ("2026-11-18", "Added a box-to-row exercise: remove a candidate without choosing between two possible cells."),
        "how-to-find-web-games-that-fit-short-breaks": ("2026-11-18", "Added a checklist for a browser game that will not load, starting with checks that leave saved progress alone."),
        "number-block-or-color-puzzles-for-your-break": ("2026-11-18", "Added a quick check for telling pieces apart and reading move feedback without relying on color alone."),
        "how-to-choose-a-new-mobile-game-for-quick-sessions": ("2026-11-18", "Added a three-move check for control reach, screen visibility, and playing without sound."),
        "new-indie-games-for-relaxing-breaks": ("2026-11-18", "Added a way to decide whether an indie demo is worth revisiting after a developer update."),
        "how-casual-players-can-choose-new-puzzle-games": ("2026-11-18", "Added a way to use a small hint without revealing the answer, with an existing Sudoku exercise to try it on."),
    }
    listing = UpdateLinks(public / "updates/index.html")
    destinations = {title[0]: [href.split("#", 1)[1], label]
                    for title, *links in listing.rows + listing.earlier for href, label in links}
    found = set()
    link_count = 0
    for path in public.rglob("*.html"):
        notice = Notices(path.read_text())
        if path == public / "blog/index.html":
            assert sorted(notice.compact_dates) == sorted(x[0] for x in expected.values())
            assert not notice.notes and not notice.links
            continue
        assert not notice.compact_dates
        if notice.notes:
            slug = path.parent.name
            assert slug in expected, path
            date, note = expected[slug]
            assert notice.dates == [date] and len(notice.notes) == 1
            assert notice.notes[0].strip().endswith(": " + note)
            jump = destinations.get(f"/blog/{slug}/")
            if jump:
                anchor, label = jump
                href = f"#{anchor}"
                has_shortcut = any(target == href for target, _ in Shortcuts(path).links)
                assert notice.links == ([] if has_shortcut else [[href, label]]), path
            else:
                assert not notice.links, path
            link_count += len(notice.links)
            found.add(slug)
    assert found == set(expected)
    assert link_count == 7
    print(f"PASS: {len(expected)} dated article notices, {link_count} direct section links and unchanged compact archive scope")
    fixtures(root)


if __name__ == "__main__":
    main()
