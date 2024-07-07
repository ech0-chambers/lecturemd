import yaml
from pathlib import Path
import shutil
from rich.prompt import Confirm
from rich import print as rprint
import argparse

from ..platform import Platform, get_platform

operating_system = get_platform()

pandoc_crossref = "$lecturemd/pandoc-crossref" if operating_system == Platform.LINUX else "$lecturemd/pandoc-crossref.exe" if operating_system == Platform.WINDOWS else "$lecturemd/pandoc-crossref-macos" if operating_system == Platform.MAC else "$lecturemd/pandoc-crossref"

base_settings = {
    "general": {
        "colour scheme": "urban",
        "title": "Your Title",
        "subtitle": "Subtitle",
        "author": "Your Name",
        "date": "today",
        "institution": "Your Institution",
        "use pyndoc": True,
        "preamble": [],
        "maths preamble": ["preamble/maths.tex"],
        "filters": [
            "$lecturemd/notesslides.py",
            "$lecturemd/format_filter.py",
            {pandoc_crossref: 10},
        ],
        "main file": "main.md",
        "logo": {"main logo": None, "footer logo": None},
    },
    "latex": {
        "figure extension": "pdf",
        "preamble": ["preamble/latex.tex"],
        "filters": ["$lecturemd/latex_environments.py"],
        "notes": {
            "preamble": ["preamble/latex_notes.tex"],
            "filters": [{"$lecturemd/delistify.py": -10}, {"$lecturemd/derule.py": -9}],
        },
        "slides": {"preamble": ["preamble/latex_slides.tex"], "filters": []},
    },
    "html": {
        "figure extension": "svg",
        "preamble": ["preamble/html.html"],
        "filters": ["$lecturemd/html_tcolorbox.py"],
        "styles": [],
        "notes": {
            "preamble": ["preamble/html_notes.html"],
            "filters": [{"$lecturemd/delistify.py": -10}, {"$lecturemd/derule.py": -9}],
            "styles": ["styles/notes.css"],
        },
        "slides": {
            "preamble": ["preamble/html_slides.html"],
            "filters": [],
            "styles": ["styles/slides.css"],
        },
    },
}

directory_structure = {
    "files": ["main.md"],
    "directories": {
        ".lecturemd": {
            "files": [
                {
                    "name": "lecturemd.yaml",
                    "content": yaml.dump(base_settings, default_flow_style=False),
                },
            ],
            "directories": {"templates": {}},
        },
        # "filters": {},
        "sections": {},
        "styles": {},
        "figures": {},
        "preamble": {
            "files": [
                {
                    "name": "latex.tex",
                    "content": rf"""% {'-'*80}
% This preamble is applied to all LaTeX files
% This includes the pdf notes and the pdf slides.
% This is applied *before* the `latex_notes.tex` and `latex_slides.tex` files.
% You may safely remove these comments.
% {'-'*80}

""",
                },
                {
                    "name": "latex_notes.tex",
                    "content": rf"""% {'-'*80}
% This preamble is applied to the LaTeX notes only (i.e, the pdf notes).
% This is applied *after* the `latex.tex` file.
% You may safely remove these comments.
% {'-'*80}

""",
                },
                {
                    "name": "latex_slides.tex",
                    "content": rf"""% {'-'*80}
% This preamble is applied to the LaTeX slides only (i.e, the pdf slides).
% This is applied *after* the `latex.tex` file.
% You may safely remove these comments.
% {'-'*80}

""",
                },
                {
                    "name": "html.html",
                    "content": rf"""<!--{'-'*80}
This preamble is applied to the HTML notes and slides. 
This is applied *before* the `html_notes.html` and `html_slides.html` files.
You may safely remove these comments.
{'-'*80}--->

""",
                },
                {
                    "name": "html_notes.html",
                    "content": rf"""<!--{'-'*80}
This preamble is applied to the HTML notes only.
This is applied *after* the `html.html` file.
You may safely remove these comments.
{'-'*80}--->

""",
                },
                {
                    "name": "html_slides.html",
                    "content": rf"""<!--{'-'*80}
This preamble is applied to the HTML slides only.
This is applied *after* the `html.html` file.
You may safely remove these comments.
{'-'*80}--->

""",
                },
                {
                    "name": "maths.tex",
                    "content": rf"""% {'-'*80}
% This preamble is applied to all files.
% For LaTeX files, it is applied directly.
% For html files, it is inserted in a maths block for MathJax.
% It is applied *last* before the body of the document.
% You may safely remove these comments.
% {'-'*80}

""",
                },
            ]
        },
    },
}


def create_directory_structure(root_dir, directory_structure):
    if "files" in directory_structure:
        for file in directory_structure["files"]:
            if isinstance(file, dict):
                file_path = root_dir / file["name"]
                file_path.touch()
                with open(file_path, "w") as f:
                    f.write(file["content"])
            else:
                Path(root_dir / file).touch()
    if "directories" in directory_structure:
        for directory in directory_structure["directories"]:
            Path(root_dir / directory).mkdir()
            create_directory_structure(
                root_dir / directory, directory_structure["directories"][directory]
            )


def copy_templates(templates_dir):
    templates_src = Path(__file__).parent / "templates"
    if not templates_src.exists():
        raise FileNotFoundError(f'Templates directory "{templates_src}" does not exist')
    if not templates_src.is_dir():
        raise FileNotFoundError(
            f'Templates directory "{templates_src}" is not a directory'
        )
    # copy the entire directory
    shutil.copytree(templates_src, templates_dir, dirs_exist_ok=True)


def copy_styles(styles_dir):
    styles_src = Path(__file__).parent / "styles"
    if not styles_src.exists():
        raise FileNotFoundError(f'Styles directory "{styles_src}" does not exist')
    if not styles_src.is_dir():
        raise FileNotFoundError(f'Styles directory "{styles_src}" is not a directory')
    # copy the entire directory
    shutil.copytree(styles_src, styles_dir, dirs_exist_ok=True)


def main(target_dir: Path, interactive: bool = False, overwrite: bool = False):
    if target_dir.exists():
        if overwrite:
            shutil.rmtree(target_dir)
        else:
            if interactive:
                if Confirm.ask(f'Directory "{target_dir}" already exists. Overwrite?'):
                    shutil.rmtree(target_dir)
                else:
                    rprint("Aborting")
                    return
            else:
                raise FileExistsError(f'Directory "{target_dir}" already exists')
    target_dir.mkdir()
    create_directory_structure(target_dir, directory_structure)
    copy_templates(target_dir / ".lecturemd" / "templates")
    copy_styles(target_dir / "styles")


def parse_args():
    # python3 -m lecturemd.create [--non-interactive|-I] [--overwrite|-o] target_dir
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "target_dir", type=Path, help="The directory to create the lecture in"
    )
    parser.add_argument(
        "--non-interactive",
        "-I",
        action="store_true",
        help="Do not ask for confirmation,and exit if the target directory already exists",
    )
    parser.add_argument(
        "--overwrite",
        "-o",
        action="store_true",
        help="Overwrite the target directory if it already exists, without asking for confirmation",
    )
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    main(args.target_dir, args.non_interactive, args.overwrite)
