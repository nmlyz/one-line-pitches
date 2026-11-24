"""One-line pitch writer.

Writes a single persuasive sentence to ``entry.txt`` inside the output
directory. The sentence is aimed at a friend who has never written code:
it tells them to describe their app idea to an agent on make.fun and have
a first version to tap tonight, and it is honest up front that the first
version will not be perfect, with every flaw fixable in a sentence.

Only the Python standard library is used. Running the program twice
produces byte-identical output.
"""

import os
import sys

# The pitch itself. One sentence, 201 characters, ending in a period.
PITCH = (
    "The first version won't be perfect and that's the point, "
    "tell an agent on make.fun what your app should do and "
    "tonight you'll have something real to tap, and every flaw "
    "is yours to fix with a sentence."
)

MAX_CHARS = 240
MIN_CHARS = 1
OUTPUT_NAME = "entry.txt"


def die(message):
    """Print an error and stop with a non-zero exit code."""
    print("error: " + message, file=sys.stderr)
    raise SystemExit(1)


def check_pitch(text):
    """Refuse any text that would fail the competition gate."""
    if not isinstance(text, str):
        die("pitch is not text")
    if not text.strip():
        die("pitch is blank")
    if len(text) < MIN_CHARS or len(text) > MAX_CHARS:
        die("pitch must be %d to %d characters, got %d"
            % (MIN_CHARS, MAX_CHARS, len(text)))
    if "\n" in text or "\r" in text:
        die("pitch must be a single line")
    if "  " in text:
        die("pitch must not contain double spaces")
    if "?" in text or "!" in text:
        die("pitch must not contain a question mark or exclamation mark")
    if not text.endswith("."):
        die("pitch must end with a period")
    # "make.fun" holds a period of its own, so ignore it when counting
    # sentence-ending periods: only the final one may remain.
    without_domain = text.replace("make.fun", "")
    if without_domain.count(".") != 1:
        die("pitch must be exactly one sentence")
    if not without_domain.endswith("."):
        die("pitch must end with its only period")


def write_entry(text, out_dir):
    """Write the pitch as UTF-8 text and report its length."""
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, OUTPUT_NAME)
    with open(path, "w", encoding="utf-8", newline="") as handle:
        handle.write(text)
    # Only the file itself gets its mode set, never the directory.
    os.chmod(path, 0o644)
    print("wrote %d characters to %s" % (len(text), path))
    return path


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    check_pitch(PITCH)
    write_entry(PITCH, out_dir)


if __name__ == "__main__":
    main()
