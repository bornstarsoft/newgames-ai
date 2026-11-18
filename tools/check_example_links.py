#!/usr/bin/env python3
"""Validate native, stable example links without disclosing answers."""
from html.parser import HTMLParser
import json
from pathlib import Path
import sys

from check_updates import Page


class Examples(HTMLParser):
    def __init__(self, html):
        super().__init__()
        self.items = []
        self.current = None
        self.in_heading = False
        self.in_answer = False
        self.feed(html)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "section" and attrs.get("class") in ("sudoku-check", "block-check"):
            self.current = dict(id=attrs["id"], label=attrs["aria-labelledby"], headings=[], links=[], text="", details=0,
                                answer_links=[], board_targets=[])
            self.items.append(self.current)
        if self.current is not None:
            if tag == "h3":
                self.in_heading = True
                self.current["headings"].append(attrs["id"])
            if tag == "a":
                assert self.in_heading or self.in_answer
                self.current["links" if self.in_heading else "answer_links"].append(attrs)
            if tag == "table" and "id" in attrs:
                assert not self.in_answer and attrs.get("tabindex") == "-1"
                self.current["board_targets"].append(attrs["id"])
            if tag == "details":
                assert "open" not in attrs
                self.in_answer = True
                self.current["details"] += 1

    def handle_data(self, text):
        if self.in_heading and self.current is not None:
            self.current["text"] += text

    def handle_endtag(self, tag):
        if tag == "h3": self.in_heading = False
        if tag == "details": self.in_answer = False
        if tag == "section": self.current = None


def main():
    root = Path(__file__).resolve().parent.parent
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "public"
    cases = [
        ("how-to-find-your-first-sudoku-move", "sudoku_practice", "check"),
        ("sudoku-one-place-for-a-number", "sudoku_places", "place"),
        ("block-puzzle-fit-clear-leave-space", "block_practice", "check"),
    ]
    count = 0
    for slug, datafile, prefix in cases:
        route = f"/blog/{slug}/"
        path = public / route.lstrip("/") / "index.html"
        data = json.loads((root / f"data/{datafile}.json").read_text())
        page = Page(path)
        examples = Examples(path.read_text()).items
        assert [e["id"] for e in examples] == [f"{prefix}-{key}" for key in data]
        for item, example in zip(data.values(), examples):
            assert example["headings"] == [example["label"]]
            assert example["text"] == item["title"]
            assert len(example["links"]) == example["details"] == 1
            link = example["links"][0]
            assert link["href"] == route + "#" + example["id"]
            assert link["title"] == "Link to this example"
            assert not ({"target", "download", "onclick"} & link.keys())
            assert example["id"] in page.ids
            if datafile == "block_practice":
                board = "start-board-" + example["id"].removeprefix("check-")
                assert example["board_targets"] == [board] and board in page.ids
                assert example["answer_links"] == [{"href": "#" + board}]
            else:
                assert not example["board_targets"] and not example["answer_links"]
            count += 1
        assert page.canonical == "https://newgames.ai" + route
        assert all(s.get("type") == "application/ld+json" for s in page.scripts)
    assert count == 9
    for filename in ("index.html", "blog/index.html", "updates/index.html"):
        assert not Examples((public / filename).read_text()).items
    print("PASS: nine stable example links, four closed-answer links to focusable start boards, no new script or homepage controls")


if __name__ == "__main__":
    main()
