#!/usr/bin/env python3
"""Check contextual learning links without introducing game-feature promises."""
from pathlib import Path
import sys

from check_updates import Page


def main():
    public = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).resolve().parent.parent / "public"
    cases = [
        (
            "daysudoku-free-daily-sudoku-game-online",
            "practice-finding-a-starting-move",
            ["how-to-find-your-first-sudoku-move", "sudoku-one-place-for-a-number"],
            "https://daysudoku.com/",
            "not answers to DaySudoku",
        ),
        (
            "blockzzle-free-block-puzzle-game-online",
            "practice-a-placement-decision",
            ["block-puzzle-fit-clear-leave-space"],
            "https://blockzzle.com/play/",
            "not Blockzzle levels",
        ),
        (
            "ringzzle-free-color-rings-puzzle-game-online",
            "before-ending-a-session",
            ["browser-game-save-progress-checklist"],
            "https://ringzzle.com/play/",
            "not a claim about what Ringzzle saves",
        ),
    ]
    for slug, section, guides, play, boundary in cases:
        path = public / "blog" / slug / "index.html"
        page = Page(path)
        assert section in page.ids, f"Missing section: {slug}"
        assert play in page.links, f"Official play link lost: {slug}"
        assert boundary in path.read_text(), f"Missing scope boundary: {slug}"
        assert page.canonical == f"https://newgames.ai/blog/{slug}/"
        for guide in guides:
            route = f"/blog/{guide}/"
            assert route in page.links, f"Missing learning path: {slug} -> {guide}"
            target = public / "blog" / guide / "index.html"
            assert target.is_file(), f"Unpublished destination: {guide}"
            if guide in ("how-to-find-your-first-sudoku-move", "block-puzzle-fit-clear-leave-space"):
                assert f"/blog/{slug}/" in Page(target).links, f"Missing return link: {guide}"
    print("PASS: three introduction sections, four published guide links, official play links, scope boundaries and two return paths")


if __name__ == "__main__":
    main()
