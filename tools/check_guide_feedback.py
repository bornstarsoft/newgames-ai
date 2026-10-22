#!/usr/bin/env python3
"""Validate contextual email links without sending mail or collecting data."""
from html.parser import HTMLParser
from pathlib import Path
import sys
from urllib.parse import parse_qs, urlsplit

from check_updates import Page


TARGETS = {
    "how-to-find-your-first-sudoku-move",
    "block-puzzle-fit-clear-leave-space",
    "browser-game-save-progress-checklist",
    "number-block-or-color-puzzles-for-your-break",
    "sudoku-one-place-for-a-number",
    "return-to-a-puzzle-after-a-break",
}


class Feedback(HTMLParser):
    def __init__(self, path):
        super().__init__()
        self.count = 0
        self.inside = self.in_title = False
        self.title = ""
        self.links = []
        self.email_off = False
        self.email_markers = []
        self.feed(path.read_text())

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "h1": self.in_title = True
        if tag == "aside" and attrs.get("class") == "guide-feedback":
            self.count += 1
            self.inside = True
            assert self.title, "Feedback must follow the article heading"
            assert attrs.get("aria-labelledby") == "guide-feedback-title"
        if self.inside:
            assert tag not in {"script", "form", "input", "iframe"}
            if tag == "a":
                if attrs["href"].startswith("mailto:"):
                    assert self.email_off, "Email must retain its Cloudflare exclusion markers"
                self.links.append(attrs["href"])

    def handle_comment(self, data):
        if data == "email_off":
            assert not self.email_off
            self.email_off = True
        elif data == "/email_off":
            assert self.email_off
            self.email_off = False
        else:
            raise AssertionError(f"Unexpected public HTML comment: {data}")
        self.email_markers.append(data)

    def handle_data(self, data):
        if self.in_title: self.title += data

    def handle_endtag(self, tag):
        if tag == "h1": self.in_title = False
        if tag == "aside": self.inside = False


def main():
    root = Path(__file__).resolve().parent.parent
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "public"
    enabled = set()
    for path in public.rglob("*.html"):
        feedback = Feedback(path)
        assert not feedback.email_off
        if path == public / "contact/index.html" or feedback.count:
            assert feedback.email_markers == ["email_off", "/email_off"]
        else:
            assert not feedback.email_markers
        if not feedback.count: continue
        slug = path.parent.name
        assert slug in TARGETS and feedback.count == 1, path
        enabled.add(slug)
        page = Page(path)
        assert "guide-feedback-title" in page.ids
        assert len(feedback.links) == 2
        mail = urlsplit(feedback.links[0])
        assert mail.scheme == "mailto" and mail.path == "hello@newgames.ai"
        assert not mail.fragment
        assert parse_qs(mail.query) == {
            "subject": [f"NewGames.ai guide feedback: {feedback.title}"],
            "body": [f"Guide: {page.canonical}\r\n\r\nMy question or correction:\r\n"],
        }, (path, mail.query)
        assert page.canonical == f"https://newgames.ai/blog/{slug}/"
        assert feedback.links[1] == "/contact/"
        assert "css/guides.css" in path.read_text()
    assert enabled == TARGETS
    contact = Page(public / "contact/index.html")
    assert "guide-feedback" in contact.ids
    assert "mailto:hello@newgames.ai" in contact.links
    assert "/updates/" in contact.links
    for address in ("support", "games", "privacy"):
        assert f"mailto:{address}@newgames.ai" in contact.links
    print(f"PASS: {len(enabled)} scoped feedback areas, exact email context, preserved Cloudflare exclusion markers, no unexpected comments, contact fallback and existing addresses")


if __name__ == "__main__":
    main()
