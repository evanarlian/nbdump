from argparse import ArgumentParser
from pathlib import Path

from nbdump import __version__
from nbdump.core import dump

if __name__ == "__main__":
    # args
    parser = ArgumentParser()
    parser.add_argument("files", nargs="+", help="Files to write to notebook")
    parser.add_argument(
        "-o", "--out", type=Path, required=True, help="Filepath to dump (.ipynb)"
    )
    parser.add_argument(
        "-c", "--code", default=[], action="append", help="Extra code cell to add"
    )
    parser.add_argument(
        "-V", "--version", action="version", version=f"%(prog)s {__version__}"
    )
    args = parser.parse_args()

    # main cli operation
    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        dump(f, args.files, args.code)
