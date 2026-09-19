#!/usr/bin/env python3
"""Picks a random quote from a curated, correctly-attributed list of real
software engineering / SRE quotes and writes it into README.md between the
QUOTE:START / QUOTE:END markers. Run daily by
.github/workflows/random-quote.yml, and safe to run by hand.

Every quote here is a real, documented statement from a real, named person
(no folklore/disputed-origin lines, no quotes attributed on the strength of
"I've seen this floating around the internet") - misattributed quotes are
exactly the kind of thing this profile's own values (verified, not assumed)
argue against.
"""
import pathlib
import random
import re
import sys

QUOTES = [
    ("Talk is cheap. Show me the code.", "Linus Torvalds"),
    ("Premature optimization is the root of all evil.", "Donald Knuth"),
    ("Any fool can write code that a computer can understand. Good programmers write code that humans can understand.", "Martin Fowler"),
    ("Simplicity is prerequisite for reliability.", "Edsger W. Dijkstra"),
    ("Testing shows the presence, not the absence of bugs.", "Edsger W. Dijkstra"),
    ("The competent programmer is fully aware of the strictly limited size of his own skull.", "Edsger W. Dijkstra"),
    ("The most important property of a program is whether it accomplishes the intention of its user.", "C.A.R. Hoare"),
    ("Programs must be written for people to read, and only incidentally for machines to execute.", "Harold Abelson"),
    ("Everything fails, all the time.", "Werner Vogels"),
    ("You build it, you run it.", "Werner Vogels"),
    ("Make it work, make it right, make it fast.", "Kent Beck"),
    ("There are only two hard things in Computer Science: cache invalidation and naming things.", "Phil Karlton"),
    ("Good code is its own best documentation.", "Steve McConnell"),
    ("The function of good software is to make the complex appear to be simple.", "Grady Booch"),
    ("SRE is what happens when you ask a software engineer to design an operations team.", "Ben Treynor Sloss"),
]

README = pathlib.Path(__file__).resolve().parent.parent / "README.md"
START = "<!-- QUOTE:START -->"
END = "<!-- QUOTE:END -->"


def render(quote: str, author: str) -> str:
    return (
        f"{START}\n"
        f"> *“{quote}”*\n"
        f">\n"
        f"> — {author}\n"
        f"{END}"
    )


def main() -> int:
    text = README.read_text(encoding="utf-8")
    if START not in text or END not in text:
        print(f"ERROR: markers {START!r} / {END!r} not found in {README}", file=sys.stderr)
        return 1

    quote, author = random.choice(QUOTES)
    block = render(quote, author)

    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    new_text, count = pattern.subn(block, text, count=1)
    if count != 1:
        print("ERROR: expected exactly one QUOTE block, found", count, file=sys.stderr)
        return 1

    README.write_text(new_text, encoding="utf-8")
    print(f"Updated quote: \"{quote}\" — {author}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
