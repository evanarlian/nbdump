import json
import sys
from argparse import ArgumentParser, Namespace
from pathlib import Path

import nbformat as nbf


def generate_target_files(paths: list[str]) -> list[Path]:
    """
    Given a list of path:
    * If element is a dir, recursively add subfiles
    * If element is a file, add as is
    * Ignore the rest

    Args:
        root (list[str]): List of paths entered by user

    Returns:
        list[Path]: list of file path, no directories
    """
    unique_paths = set()
    for path in paths:
        path = Path(path)
        if not path.exists():
            print(f"[WARN] {path} does not exist, skipped.", file=sys.stderr)
        elif path.is_dir():
            unique_paths |= set([p for p in path.rglob("*.*") if p.is_file()])
        elif path.is_file():
            unique_paths.add(path)
        else:
            print(f"[WARN] {path} is not supported, skipped.", file=sys.stderr)
    return sorted(unique_paths)


def dedup_folders(files: list[Path]) -> list[Path]:
    """Extract parent folders from given paths"""
    unique_folders = {file.parent for file in files}
    unique_folders.discard(Path("."))
    return sorted(unique_folders)


def construct_mkdir_commands(folders: list[Path]) -> str:
    """Make mkdir commands so that %%writefile does not fail"""
    return "\n".join([f'!mkdir -p "{folder}"' for folder in folders])


def main(args: Namespace):
    files = generate_target_files(args.files)
    folders = dedup_folders(files)
    mkdir_cmds = construct_mkdir_commands(folders)

    ipynb_json = nbf.v4.new_notebook()

    # topmost mkdir cells
    if mkdir_cmds != "":
        mkdir_cell = nbf.v4.new_code_cell(mkdir_cmds)
        ipynb_json["cells"].append(mkdir_cell)

    # code cells from files
    for file in files:
        print(f"write: {file}")
        content = file.read_text()
        wf = f'%%writefile "{file}"\n{content}'.strip()
        code_cell = nbf.v4.new_code_cell(wf)
        ipynb_json["cells"].append(code_cell)

    # extra code cells
    for code in args.code:
        print(f"code: {code}")
        code_cell = nbf.v4.new_code_cell(code)
        ipynb_json["cells"].append(code_cell)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    with open(args.out, "w") as f:
        json.dump(ipynb_json, f)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("files", nargs="+", help="Files to write to notebook")
    parser.add_argument(
        "-o", "--out", type=Path, required=True, help="Filename to dump (.ipynb)"
    )
    parser.add_argument(
        "-c", "--code", default=[], action="append", help="Extra code cell to add"
    )
    # TODO quiet + version?
    args = parser.parse_args()
    main(args)
