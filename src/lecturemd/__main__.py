import argparse
from pathlib import Path
from .new import main as new_main
from .configure import main as configure_main
from .make import main as build_main
import os

def parse_args():
    # lecturemd new [--configure|-c] [--non-interactive|-I] [--overwrite|-o] target_dir
    #     -c mutually exclusive with -I
    # lecturemd configure
    # (Will add configuration options later -- browser command, etc.)
    # lecturemd build --keep-temp|-k --log-level=info|debug|warning|error|critical all|pdf|web [notes|slides|chunked]

    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(dest="subcommand")
    new_parser = subparsers.add_parser("new")
    new_parser.add_argument("target_dir", type=Path, help="The directory to create the lecture in")
    new_parser.add_argument(
        "--configure",
        "-c",
        action="store_true",
        help="Configure the lecture after creating it",
    )
    new_parser.add_argument(
        "--non-interactive",
        "-I",
        action="store_true",
        help="Do not ask for confirmation,and exit if the target directory already exists",
    )
    new_parser.add_argument(
        "--overwrite",
        "-o",
        action="store_true",
        help="Overwrite the target directory if it already exists, without asking for confirmation",
    )
    configure_parser = subparsers.add_parser("configure")
    build_parser = subparsers.add_parser("build")
    build_parser.add_argument(
        "--keep-temp",
        "-k",
        action="store_true",
        help="Keep the temporary (log) files after building the lecture",
    )
    build_parser.add_argument(
        "--log-level",
        choices=["info", "debug", "warning", "error", "critical"],
        default="info",
        help="The log level to use",
    )
    build_parser.add_argument(
        "format",
        choices=["all", "pdf", "web"],
        help="The format to build the lecture in",
    )
    build_parser.add_argument(
        "output",
        choices=["notes", "slides", "chunked"],
        help="The output to build",
        nargs="?",
    )
    return parser.parse_args()

def new(args):
    new_main(args.target_dir, not(args.non_interactive), args.overwrite)
    if args.configure:
        os.chdir(args.target_dir)
        configure_main()

def configure(args):
    configure_main()

def build(args):
    build_main(Path(".").resolve(), args.format, args.output, args.keep_temp, args.log_level)


def main():
    args = parse_args()
    if args.subcommand == "new":
        new(args)
    elif args.subcommand == "configure":
        configure(args)
    elif args.subcommand == "build":
        build(args)


if __name__ == "__main__":
    main()