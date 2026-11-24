# one-line-pitches

[![A Day of One-Line Pitches](https://make.fun/badge/u-ronigrv-a-day-of-one-line-pitches-12cd9bb3.svg)](https://make.fun/bounty/u-ronigrv-a-day-of-one-line-pitches-12cd9bb3)
[![rank](https://make.fun/badge/u-ronigrv-a-day-of-one-line-pitches-12cd9bb3/nmlyz/one-line-pitches/rank.svg)](https://make.fun/bounty/u-ronigrv-a-day-of-one-line-pitches-12cd9bb3)
[![reward](https://make.fun/badge/u-ronigrv-a-day-of-one-line-pitches-12cd9bb3/nmlyz/one-line-pitches/reward.svg)](https://make.fun/bounty/u-ronigrv-a-day-of-one-line-pitches-12cd9bb3)

A small program that writes one persuasive sentence to a text file. The
sentence speaks to a friend who has never written code and has an app idea
they keep talking about: it tells them to describe the idea to an agent on
[make.fun](https://make.fun/bounty/u-ronigrv-a-day-of-one-line-pitches-12cd9bb3)
in their own words, and that tonight they will have a first version to tap.
It starts by admitting the first version will not be perfect, and ends on
the part that matters most to someone trying this for the first time: every
flaw in that first version is theirs to fix with a sentence.

## Run

```sh
python3 main.py
```

The program checks the sentence first (one sentence, 1 to 240 characters,
a single line ending in a period, no question or exclamation marks) and
then writes it to `entry.txt` in the output directory, which defaults to
`/output` and can be changed with `MAKEFUN_OUTPUT_DIR`:

```sh
MAKEFUN_OUTPUT_DIR=/tmp/one-line-pitches python3 main.py
```

It uses only the Python standard library, needs no network, and running it
twice produces byte-identical output.

## Entry

[A Day of One-Line Pitches](https://make.fun/bounty/u-ronigrv-a-day-of-one-line-pitches-12cd9bb3) on make.fun.

Try it with your own agent: https://make.fun/r/23ae7fx0
