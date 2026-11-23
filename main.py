"""Emit a single-sentence pitch for a first app idea.

The wording is assembled from small fragments held in a tuple, joined
once, checked against a table of rules, and only then stored as
``entry.txt`` inside the directory named by ``MAKEFUN_OUTPUT_DIR``
(falling back to ``/output`` when the variable is unset).
"""

import os
import sys
from pathlib import Path

# The pitch is kept as fragments so the assembly step stays visible;
# the split points are arbitrary and carry no meaning on their own.
FRAGMENTS = (
    "Stop saving that app idea for som",
    "eday and describe it to an agent on make.fun in your own wo",
    "rds, and tonight you'll be tapping a working first vers",
    "ion, and if it's wrong, one more sentence fixes it.",
)

TARGET_BYTE_COUNT = 198
OUTPUT_FILENAME = "entry.txt"
FALLBACK_DIRECTORY = "/output"
ENVIRONMENT_VARIABLE = "MAKEFUN_OUTPUT_DIR"


def assemble_pitch() -> str:
    """Glue the fragments together into the finished pitch line."""
    return "".join(FRAGMENTS)


def rule_table(encoded: bytes, text: str):
    """Pair every acceptance rule with the complaint used on failure."""
    return [
        (len(encoded) == TARGET_BYTE_COUNT,
         "byte count drifted away from the expected total"),
        (text.endswith("."),
         "the line must close with a full stop"),
        (text.replace("make.fun", "makefun").count(".") == 1,
         "the line must stay a single sentence"),
        ("?" not in text,
         "question marks are not allowed in the pitch"),
        ("\n" not in text and "\r" not in text,
         "the pitch has to fit on one physical line"),
        (text == text.strip(),
         "stray padding surrounds the pitch"),
        ("  " not in text,
         "doubled spaces crept into the wording"),
        (all(byte < 128 for byte in encoded),
         "the pitch should remain plain ASCII"),
    ]


def complain(problems) -> int:
    """Report each broken rule on stderr and signal failure."""
    for problem in problems:
        print(f"pitch rejected: {problem}", file=sys.stderr)
    return 1


def destination() -> Path:
    """Work out where entry.txt belongs for this run."""
    folder = os.environ.get(ENVIRONMENT_VARIABLE) or FALLBACK_DIRECTORY
    return Path(folder) / OUTPUT_FILENAME


def run() -> int:
    text = assemble_pitch()
    encoded = text.encode("utf-8")

    broken = [message for ok, message in rule_table(encoded, text) if not ok]
    if broken:
        return complain(broken)

    target = destination()
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(encoded)

    # Loosen the file itself so other tools can read it; the folder
    # holding it is never touched, and a failed chmod is not fatal.
    try:
        os.chmod(target, 0o644)
    except OSError:
        pass

    reread = target.read_bytes()
    if reread != encoded:
        return complain(["the stored bytes differ from the pitch"])

    print(f"done: {target} now holds the {len(reread)}-byte pitch")
    return 0


if __name__ == "__main__":
    sys.exit(run())
