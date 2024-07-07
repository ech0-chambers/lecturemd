import shutil
from typing import List
from rich.table import Table
from rich import print as rprint
from enum import Enum
import platform
from importlib.util import find_spec


class Platform(Enum):
    LINUX = 0
    WINDOWS = 1
    MAC = 2
    JAVA = 3
    UNKNOWN = 4


def get_platform() -> Platform:
    system = platform.system()
    if system == "Linux":
        return Platform.LINUX
    elif system == "Windows":
        return Platform.WINDOWS
    elif system == "Darwin":
        return Platform.MAC
    elif system == "Java":
        return Platform.JAVA
    else:
        return Platform.UNKNOWN


operating_system = get_platform()
if operating_system == Platform.UNKNOWN:
    raise Exception(
        "Unsupported or unknown operating system. Cannot check requirements."
    )


def is_installed(program: str) -> bool:
    return shutil.which(program) is not None


def is_package_installed(package: str) -> bool:
    return find_spec(package) is not None


def red(text: str) -> str:
    return "[bold red]" + text + "[/bold red]"


def green(text: str) -> str:
    return "[bold green]" + text + "[/bold green]"


def yellow(text: str) -> str:
    return "[bold yellow]" + text + "[/bold yellow]"


def error(text: str) -> str:
    return red("Error:\t") + text


def warning(text: str) -> str:
    return yellow("Warning:\t") + text


requirements = [
    {
        "program": "pandoc",
        "installed": is_installed("pandoc"),
        "fail_message": "pandoc is not installed\n\tPlease install it from [link=https://pandoc.org/installing.html]https://pandoc.org/installing.html[/link]",
    },
    {
        "program": "pdflatex",
        "installed": is_installed("pdflatex"),
        "fail_message": "pdflatex is not installed\n\tPlease install it from [link=https://www.latex-project.org/get/]https://www.latex-project.org/get/[/link]",
    },
    {
        "program": "latexmk",
        "installed": is_installed("latexmk"),
        "fail_message": "latexmk is not installed\n\tPlease install it from [link=https://mg.readthedocs.io/latexmk.html]https://mg.readthedocs.io/latexmk.html[/link]",
    },
    {
        "program": ["pdf2svg", "inkscape"],
        "installed": [is_installed("pdf2svg"), is_installed("inkscape")],
        "fail_message": [
            "pdf2svg is not installed. Inkscape will be used instead",
            "inkscape is not installed. pdf2svg will be used instead",
        ],
        "all_fail_message": "pdf2svg and inkscape are not installed\n\tAt least one of pdf2svg or inkscape is required to convert PDF to SVG\n\tPlease install pdf2svg using `sudo apt install pdf2svg` or inkscape from [link=https://inkscape.org/release/inkscape-1.3.2/]https://inkscape.org/release/inkscape-1.3.2/[/link] (or the most recent version)",
    },
    {
        "program": "imagemagick",
        "installed": (
            is_installed("convert")
            if operating_system in [Platform.LINUX, Platform.MAC]
            else is_installed("magick")
        ),
        "fail_message": "imagemagick is not installed\n\tPlease install it from [link=https://imagemagick.org/script/download.php]https://imagemagick.org/script/download[/link]",
    },
    {
        "program": "pyndoc",
        "is_python": True,
        "installed": is_package_installed("pyndoc"),
        "fail_message": "pyndoc is not installed\n\tPlease install it by following the instructions at [link=https://github.com/ech0-chambers/pyndoc]https://github.com/ech0-chambers/pyndoc[/link].",
    },
    {
        "program": "pygmentation",
        "is_python": True,
        "installed": is_package_installed("pygmentation"),
        "fail_message": "pygmentation is not installed\n\tPlease install it by following the instructions at [link=https://github.com/ech0-chambers/pygmentation]https://github.com/ech0-chambers/pygmentation[/link].",
    },
    {
        "program": "panflute",
        "is_python": True,
        "installed": is_package_installed("panflute"),
        "fail_message": "panflute is not installed\n\tPlease install it by running `pip install panflute`.",
    },
    {
        "program": "pyaml",
        "is_python": True,
        "installed": is_package_installed("yaml"),
        "fail_message": "pyaml is not installed\n\tPlease install it by running `pip install pyaml`.",
    },
    {
        "program": "textual",
        "is_python": True,
        "installed": is_package_installed("textual"),
        "fail_message": "textual is not installed\n\tPlease install it by running `pip install textual`.",
    },
    {
        "program": "pint",
        "is_python": True,
        "installed": is_package_installed("pint"),
        "fail_message": "pint is not installed\n\tPlease install it by running `pip install pint`.",
    },
]


def check_requirements(requirements: List[dict]):
    rprint("")
    table = Table(show_header=False, show_edge=False)
    table.add_column("")
    table.add_column("", justify="center")

    for requirement in requirements:
        if isinstance(requirement["program"], str):
            table.add_row(
                (
                    requirement["program"]
                    if requirement["installed"]
                    else red(requirement["program"])
                ),
                green("\u2713") if requirement["installed"] else red("\u2717"),
            )
        else:
            for program, installed in zip(
                requirement["program"], requirement["installed"]
            ):
                table.add_row(
                    program if installed else red(program),
                    green("\u2713") if installed else red("\u2717"),
                )
    rprint(table)
    rprint("")

    all_passed = True
    for requirement in requirements:
        if isinstance(requirement["program"], list):
            if not any(requirement["installed"]):
                all_passed = False
                rprint(error(requirement["all_fail_message"]))
            else:
                for program, installed, fail_message in zip(
                    requirement["program"],
                    requirement["installed"],
                    requirement["fail_message"],
                ):
                    if not installed:
                        rprint(warning(fail_message))
        else:
            if not requirement["installed"]:
                all_passed = False
                rprint(error(requirement["fail_message"]))
    if all_passed:
        rprint(green("All requirements are satisfied"))


if __name__ == "__main__":
    check_requirements(requirements)
