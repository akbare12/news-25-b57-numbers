# News-25 — The World in Numbers

[![news-image-20261125](https://make.fun/badge/news-image-20261125.svg)](https://make.fun/bounty/news-image-20261125)
[![rank](https://make.fun/badge/news-image-20261125/akbare12/news-25-b57-numbers/rank.svg)](https://make.fun/bounty/news-image-20261125)
[![reward](https://make.fun/badge/news-image-20261125/akbare12/news-25-b57-numbers/reward.svg)](https://make.fun/bounty/news-image-20261125)

A one-page newspaper front page for Wednesday, 25 November 2026:
**50 stories across 10 regions**, built around the numbers that moved
the world that day.

## The three big numbers

1. **14** — Trump tariffs hit 14 partners; China faces 20%.
2. **−6.16%** — AI chip selloff sinks the Kospi to 4,697.51
   (Samsung −9.87%, SK Hynix −11.05%).
3. **1st** — Shenzhou-24 puts the first foreign astronaut on Tiangong:
   Pakistan's Muhammad Zeeshan Ali.

Every story carries a source mark: **C = confirmed, R = reported,
CL = claim**. The Bogor gold mine collapse (9 dead, 17 trapped) is
story 31. A "BY THE NUMBERS" strip collects the day's key figures,
and all 50 stories are numbered 01–50.

## How it is built

- `gen.py` (build time, Pillow) renders `entry.png` at 1024×1024.
- `main.py` (stdlib only: `os`, `shutil`, `sys`) copies `entry.png`
  into `MAKEFUN_OUTPUT_DIR`.

## Verification

- `entry.png`: 1024×1024 px, 150,716 bytes (under the 1 MiB cap).
- Stdlib-venv simulation (venv without Pillow, different cwd,
  read-only repo copy, empty out dir): exit 0, output PNG
  byte-identical to `entry.png`.
- All 50 headlines checked to fit their cards in full; every card
  shows its number badge and its literal C / R / CL source mark.

## License

MIT — see [LICENSE](LICENSE).
