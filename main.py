#!/usr/bin/env python3
"""NEWS-25 entry runner (stdlib only).

Copies the pre-rendered entry.png next to this file into the grader's
output directory. No third-party imports: os / shutil / sys only.
"""
import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    src = os.path.join(here, "entry.png")
    if not os.path.isfile(src):
        print("error: entry.png missing next to main.py", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "out")
    os.makedirs(out_dir, exist_ok=True)
    dst = os.path.join(out_dir, "entry.png")
    shutil.copyfile(src, dst)
    print("copied entry.png to", dst)
    return 0


if __name__ == "__main__":
    sys.exit(main())
