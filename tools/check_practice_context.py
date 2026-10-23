#!/usr/bin/env python3
"""Ensure every directly linked example includes its own reading context."""
from html.parser import HTMLParser
from pathlib import Path
import sys


class Context(HTMLParser):
    def __init__(self, markup):
        super().__init__()
        self.examples = []
        self.current = self.capture = None
        self.ids = []
        self.feed(markup)

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if "id" in attrs: self.ids.append(attrs["id"])
        if tag == "section" and attrs.get("class") in ("sudoku-check", "block-check"):
            self.current = {"id": attrs["id"], "notes": [], "tables": [], "caption": "", "answers": 0}
            self.examples.append(self.current)
        if self.current is None: return
        if tag == "p" and attrs.get("class") == "practice-context":
            assert not self.current["tables"], "Context must precede its table"
            assert not ({"hidden", "aria-hidden"} & attrs.keys())
            self.current["notes"].append([attrs["id"], ""])
            self.capture = "note"
        if tag == "table": self.current["tables"].append(attrs.get("aria-describedby"))
        if tag == "caption": self.capture = "caption"
        if tag == "details":
            assert "open" not in attrs
            self.current["answers"] += 1

    def handle_data(self, data):
        if self.current is None: return
        if self.capture == "note": self.current["notes"][-1][1] += data
        if self.capture == "caption": self.current["caption"] += data

    def handle_endtag(self, tag):
        if tag in ("p", "caption"): self.capture = None
        if tag == "section": self.current = None


def main():
    root = Path(__file__).resolve().parent.parent
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else root / "public"
    cases = [
        ("how-to-find-your-first-sudoku-move", 3, ["not a full puzzle", "sorted visible digits", "one empty cell", "not board positions", "more than one group"]),
        ("sudoku-one-place-for-a-number", 2, ["every empty cell in one row", "not a full puzzle", "Column labels identify positions", "all digits allowed", "row, column and box checks"]),
        ("block-puzzle-fit-clear-leave-space", 3, ["whole piece on empty cells", "without rotating", "rows and columns clear together", "other cells do not fall", "stated piece order", "these examples only"]),
    ]
    for slug, count, phrases in cases:
        parsed = Context((public / "blog" / slug / "index.html").read_text())
        assert len(parsed.ids) == len(set(parsed.ids))
        assert len(parsed.examples) == count
        for example in parsed.examples:
            assert len(example["notes"]) == example["answers"] == 1
            note_id, note = example["notes"][0]
            assert note_id == "context-" + example["id"]
            assert example["tables"] == [note_id]
            assert all(phrase in note for phrase in phrases), (slug, note)
            if slug.startswith("block-"):
                assert all(s in example["caption"] for s in ("4-by-4", "X = occupied", "dot = empty", "left to right", "top to bottom"))
    for route in ("index.html", "blog/index.html", "updates/index.html"):
        assert not Context((public / route).read_text()).examples
    print("PASS: eight visible pre-table context notes, unique described-by targets, reading/rule boundaries and closed answers; no directory/home additions")


if __name__ == "__main__":
    main()
