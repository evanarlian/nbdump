import json
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
        if path.is_dir():
            unique_paths |= set(path.rglob("*.*"))
        else:
            unique_paths.add(path)
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
    mkdir_cell = nbf.v4.new_code_cell(mkdir_cmds)
    ipynb_json["cells"].append(mkdir_cell)

    # code cells from files
    for file in files:
        content = file.read_text()
        wf = f'%%writefile "{file}"\n{content}'.strip()
        code_cell = nbf.v4.new_code_cell(wf)
        ipynb_json["cells"].append(code_cell)

    # extra code cells
    for code in args.code:
        code_cell = nbf.v4.new_code_cell(code)
        ipynb_json["cells"].append(code_cell)

    with open(args.out, "w") as f:
        json.dump(ipynb_json, f)


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("out", type=Path, help="Filename to dump (.ipynb)")
    parser.add_argument("files", nargs="+", help="Files to write to notebook")
    parser.add_argument(
        "-c", "--code", default=[], action="append", help="Extra code cell to add"
    )
    args = parser.parse_args()
    print(args)
    main(args)
