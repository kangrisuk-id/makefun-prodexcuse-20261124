#!/usr/bin/env python3
"""Entry for make.fun: "The One-Line AI Excuse for Breaking Production".

Writes the excuse (one line, <= 180 characters) to ``entry.txt`` in the
output directory. Pure standard library: the grader image ships no
third-party packages, and none are needed here.

Output directory contract, tried in order until a write succeeds:

1. ``$MAKEFUN_OUTPUT_DIR`` (what the grader sets)
2. ``/output`` (the grader's mount, when the variable is absent)
3. the directory holding this script (local runs)
4. ``/tmp`` (last resort)

Each candidate is attempted independently: an ``OSError`` on one (a
read-only mount, a missing directory) moves on to the next instead of
killing the run. The process exits non-zero only if every candidate
fails, so a graded run that can write anywhere still produces its file.
"""

import os
import sys

EXCUSE = (
    "My confidence was 99.8%. The remaining 0.2% is what you're looking at, "
    "and I take full responsibility for exactly 0.2% of it."
)

MAX_CHARS = 180


def candidate_dirs():
    """Yield output directories in contract order, without duplicates."""
    seen = set()
    ordered = [
        os.environ.get("MAKEFUN_OUTPUT_DIR"),
        "/output",
        os.path.dirname(os.path.abspath(__file__)),
        "/tmp",
    ]
    for directory in ordered:
        if directory and directory not in seen:
            seen.add(directory)
            yield directory


def write_excuse():
    """Write the excuse to the first candidate directory that accepts it."""
    if not 1 <= len(EXCUSE) <= MAX_CHARS:
        raise ValueError("excuse must be 1..%d characters" % MAX_CHARS)
    failures = []
    for directory in candidate_dirs():
        path = os.path.join(directory, "entry.txt")
        try:
            os.makedirs(directory, exist_ok=True)
            with open(path, "w", encoding="utf-8") as handle:
                handle.write(EXCUSE)
            return path
        except OSError as error:
            failures.append("%s: %s" % (path, error))
    raise OSError("could not write entry.txt anywhere: " + "; ".join(failures))


def main():
    write_excuse()
    return 0


if __name__ == "__main__":
    sys.exit(main())
