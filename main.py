#!/usr/bin/env python3
"""one-line-pitches: write one pitch sentence to entry.txt.

The sentence is aimed at one friend who has never written code. They
have brought up the same app idea a dozen times, so the pitch asks them
to describe it to an agent in their own words and be tapping a working
first version tonight — and to know that changing their mind costs
nothing. The low-risk turn is the closing beat, not a summary or slogan.

Standard library only, no network. Deterministic: identical bytes on
every run.
"""

import os
import sys

# The sentence is assembled from three clauses, one per beat of the
# pitch, so each beat can be checked on its own: the shared history, the
# concrete ask with tonight's payoff, then the low-risk turn that closes it.
CLAUSES = (
    "You've told me about that app idea a dozen times,",
    "so describe it to an agent on make.fun in your own words and tonight you'll be tapping a working first version,",
    "and changing your mind costs nothing.",
)

LINE = " ".join(CLAUSES)

MIN_LEN = 1
MAX_LEN = 240


def problems(text: str) -> list:
    """Return every gate violation for the entry text (empty means valid)."""
    found = []
    if not (MIN_LEN <= len(text) <= MAX_LEN):
        found.append(f"entry is {len(text)} code points, must be {MIN_LEN}-{MAX_LEN}")
    stripped = text.strip()
    if not stripped:
        found.append("entry must not be only white space")
    if text != stripped:
        found.append("entry must not start or end with white space")
    if "\n" in text or "\r" in text:
        found.append("entry must be a single line")
    if "  " in text:
        found.append("entry must not contain a double space")
    if not stripped.endswith("."):
        found.append("entry must end as one sentence")
    return found


def main() -> int:
    if len(CLAUSES) != 3:
        print("pitch must be built from exactly three clauses", file=sys.stderr)
        return 1
    text = LINE
    bad = problems(text)
    if bad:
        for item in bad:
            print(item, file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(text)
    # chmod is best-effort: in the grading sandbox /output is a root-owned
    # mount and the program runs as uid 65534, so chmod there raises EPERM.
    # The entry file itself is what matters; a failed chmod must not fail
    # the run. (The output directory itself is never chmodded or removed.)
    try:
        os.chmod(path, 0o644)
    except OSError:
        pass
    # Read the file back as bytes and confirm they match the pitch exactly.
    with open(path, "rb") as f:
        if f.read() != text.encode("utf-8"):
            print("entry.txt does not match the pitch sentence", file=sys.stderr)
            return 1
    print(f"wrote {len(text)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
