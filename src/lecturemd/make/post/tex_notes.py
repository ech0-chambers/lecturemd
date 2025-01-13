#!/usr/bin/env python3

import sys
from pathlib import Path
import re

def fixed_figures(content: str) -> str:
    for matched in re.finditer(
        r"\\begin\{fixedfigure\}\s*\\begin\{figure\}(\[.*?\])?(.*?)\\end\{figure\}\s*\\end\{fixedfigure\}",
        content,
        re.DOTALL,
    ):
        content = content.replace(
            matched.group(0), "\\begin{figure}[H]\n" + matched.group(2) + "\n\\end{figure}"
        )

    return content

def split_to_align(content: str) -> str:
    # turn `\[\begin{split} ... \end{split}\]` into `\begin{align*} ... \end{align*}`
    for matched in re.finditer(
        r"\\\[\s*\\begin\{split\}(.*?)\\end\{split\}\s*\\]",
        content,
        re.DOTALL,
    ):
        content = content.replace(
            matched.group(0), "\\begin{align*}" + matched.group(1) + "\\end{align*}"
        )

    return content

replacements = [
    (r"(?P<letter>\w)\s*(?P<script>\\text(sub|super)script)", r"\g<letter>\g<script>"),
]

def spacing(content: str) -> str:
    for rep in replacements:
        if len(rep) == 3:
            pattern, replacement, flags = rep
        else:
            pattern, replacement = rep
            flags = 0
        content = re.sub(pattern, replacement, content, flags=flags)
    return content

functions = [fixed_figures, split_to_align, spacing]


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

    for func in functions:
        content = func(content)

    with file.open("w") as f:
        f.write(content)


if __name__ == "__main__":
    main()
