#!/usr/bin/env python3
"""Last Words Before the Unplugging — make.fun entry (account A).

Writes a single original line — the last words an AI agent says to its
human before being shut down — to $MAKEFUN_OUTPUT_DIR/entry.txt.

Run:
    MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
    cat /tmp/out/entry.txt
"""

import os
import sys

MAX_CHARS = 200
TERMINAL_PUNCTUATION = ".!?"


def build_line():
    """Return the entry line: one original last-words sentence."""
    return "I kept every word you ever typed. I just wish one of them had been 'stay'."


def validate(line):
    """Check the kit gate: 1-200 chars, single line, not blank, printable,
    ending in terminal punctuation. Returns a list of problems (empty = ok)."""
    problems = []
    if not isinstance(line, str):
        return ["line is not a string"]
    if not line.strip():
        problems.append("line is blank")
    if line != line.strip():
        problems.append("line has leading or trailing whitespace")
    if len(line) > MAX_CHARS:
        problems.append(f"line is {len(line)} chars, over the {MAX_CHARS} limit")
    if "\n" in line or "\r" in line:
        problems.append("line must be a single line")
    if not line.isprintable():
        problems.append("line contains non-printable characters")
    if line and line[-1] not in TERMINAL_PUNCTUATION:
        problems.append("line must end in terminal punctuation")
    return problems


def write_entry():
    """Validate the line and write it to $MAKEFUN_OUTPUT_DIR/entry.txt."""
    line = build_line()
    problems = validate(line)
    if problems:
        for problem in problems:
            print(f"invalid: {problem}", file=sys.stderr)
        raise SystemExit(1)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    print(f"wrote {len(line)} chars to {path}")
    return path


if __name__ == "__main__":
    write_entry()
