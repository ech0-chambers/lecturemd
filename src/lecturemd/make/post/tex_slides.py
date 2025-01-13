#!/usr/bin/env python3

import sys
from pathlib import Path
import re


def paused_align(content: str) -> str:

    pattern = r"\\begin\{(?:split|align\*?)\}(.*?)\\end\{(?:split|align\*?)\}"

    for matched in re.finditer(pattern, content, re.DOTALL):
        # replace any `\\` with `\Pause\\`
        new_content = matched.group(1).replace(r"\\", r"\Pause\\")
        # replace the old content with the new content
        content = content.replace(matched.group(1), new_content)

    return content


def main():
    if len(sys.argv) != 2:
        print("Usage: tex_notes.py <file>")
        sys.exit(1)

    file = Path(sys.argv[1])
    if not file.is_file():
        print(f"File {file} not found")
        sys.exit(1)

    with file.open("r") as f:
        content = f.read()

    content = paused_align(content)

    with file.open("w") as f:
        f.write(content)


if __name__ == "__main__":
    main()