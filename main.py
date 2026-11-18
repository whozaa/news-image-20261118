"""News Image 18 Nov 2026 — entry program.

Copies the pre-generated infographic entry.png (in this repository)
to /output/entry.png, deterministically.

Standard library only. No network, no timestamps, no randomness.
The output is byte-identical on every run because it is a plain
copy of a fixed file.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    # In the make.fun sandbox the output directory is /output.
    # MAKEFUN_OUTPUT_DIR is honoured only so the program can be
    # tested locally into a scratch directory; it changes no bytes.
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    src = os.path.join(HERE, "entry.png")
    if not os.path.isfile(src):
        raise SystemExit("entry.png is missing next to main.py")
    dst = os.path.join(output_dir, "entry.png")
    shutil.copyfile(src, dst)


if __name__ == "__main__":
    main()
