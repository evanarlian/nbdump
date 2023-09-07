import json
import sys
from argparse import ArgumentParser, Namespace
from copy import deepcopy
from pathlib import Path

from templates import CELL, IPYNB_JSON, WF


def generate_target_files(root: Path) -> list[Path]:
    files = list(root.rglob("*.py"))
    return files


def unique_folders(files: list[Path]) -> list[Path]:
    folders = set()
    for file in files:
        folders.add(file.parent)
    folders.discard(Path("."))
    return sorted(folders)


def construct_mkdir_commands(folders: list[Path]) -> str:
    templates = []
    for folder in folders:
        templates.append(f"!mkdir -p {repr(str(folder))}")
    return "\n".join(templates)


def dump_ipynb(ipynb_json, path):
    if path is None:
        json.dump(ipynb_json, sys.stdout, indent=2)
    else:
        with open(path, "w") as f:
            json.dump(ipynb_json, f)


def main(args: Namespace):
    files = generate_target_files(args.root)
    folders = unique_folders(files)
    mkdir_cmds = construct_mkdir_commands(folders)

    ipynb_json = deepcopy(IPYNB_JSON)

    # topmost mkdir cells
    mkdir_cell = deepcopy(CELL)
    mkdir_cell["source"] = mkdir_cmds
    ipynb_json["cells"].append(mkdir_cell)

    # code cells
    for file in files:
        content = file.read_text()
        file_cell = deepcopy(CELL)
        file_cell["source"] = WF.format(file, content).strip()
        ipynb_json["cells"].append(file_cell)

    # output ipynb
    dump_ipynb(ipynb_json, args.out)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("root", type=Path, help="Recursively dump from this directory")
    parser.add_argument(
        "-o", "--out", type=str, help="Filename to dump (.ipynb), defaults to stdout"
    )
    args = parser.parse_args()
    main(args)
