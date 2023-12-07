import json
import sys
from io import StringIO, TextIOBase
from pathlib import Path

import nbformat as nbf


def generate_target_files(paths: list[str | Path]) -> list[Path]:
    """Given a list of path:
    * If element is a dir, recursively add subfiles
    * If element is a file, add as is
    * Ignore the rest

    Args:
        root (list[str]): list of paths entered by user

    Returns:
        list[Path]: list of file path, no directories
    """
    unique_paths = set()
    for path in paths:
        path = Path(path)
        if not path.exists():
            raise FileNotFoundError(f"{path} does not exist.")
        elif path.is_dir():
            unique_paths |= set([p for p in path.rglob("*.*") if p.is_file()])
        elif path.is_file():
            unique_paths.add(path)
        else:
            print(f"[WARN] {path} is not supported, skipped.", file=sys.stderr)
    return sorted(unique_paths)


def get_parent_folders(files: list[Path]) -> list[Path]:
    """Collects all parent folders from given paths. Ignores current dir (.)

    Args:
        files (list[Path]): file paths

    Returns:
        list[Path]: parent directories
    """
    # Extract parent folders from given paths
    unique_folders = {file.parent for file in files}
    unique_folders.discard(Path("."))
    return sorted(unique_folders)


def make_mkdir_commands(folders: list[Path]) -> str:
    """Generate mkdir commands for jupyter notebook so that %%writefile
    writes to existing directory.

    Args:
        folders (list[Path]): directories to be created

    Returns:
        str: mkdir commands for jupyter notebook cells
    """
    return "\n".join([f'!mkdir -p "{folder}"' for folder in folders])


def extract_metadata(f: TextIOBase) -> dict:
    """Return metadata from ipynb (jupyter notebook).

    Args:
        f (TextIOBase): file-like object for json

    Returns:
        dict: extracted metadata
    """
    ipynb = json.load(f)
    return ipynb.get("metadata", {})


def dump(
    f: TextIOBase,
    paths: list[str | Path],
    codes: list[str] | None = None,
    metadata: str | Path | None = None,
) -> None:
    """Dump files and extra code cells to jupyter notebook.
    Files will be added as is, directories will recursively include,
    and ignore anything else.

    Args:
        f (TextIOBase): File-like object for json
        paths (list[str  |  Path]): Files or directories for dumping
        codes (list[str] | None, optional): Extra code cell to append to notebook
        metadata (str | Path | None, optional): Notebook filepath to copy metadata from
    """
    if isinstance(paths, (str, Path)):
        raise TypeError("paths must be iterable, but not string or Path")
    if isinstance(codes, str):
        raise TypeError("codes must be iterable, but not string")
    if codes is None:
        codes = []

    files = generate_target_files(paths)
    folders = get_parent_folders(files)
    mkdir_cmds = make_mkdir_commands(folders)
    ipynb = nbf.v4.new_notebook()

    # clone metadata from another notebook
    if metadata is not None:
        with open(metadata, "r") as meta:
            ipynb["metadata"] = extract_metadata(meta)

    # topmost mkdir cells
    if mkdir_cmds != "":
        mkdir_cell = nbf.v4.new_code_cell(mkdir_cmds)
        ipynb["cells"].append(mkdir_cell)

    # code cells from files
    for file in files:
        print(f"write: {file}")
        content = file.read_text()
        wf = f'%%writefile "{file}"\n{content}'.strip()
        code_cell = nbf.v4.new_code_cell(wf)
        ipynb["cells"].append(code_cell)

    # extra code cells
    for code in codes:
        print(f"code: {code}")
        code_cell = nbf.v4.new_code_cell(code)
        ipynb["cells"].append(code_cell)

    json.dump(ipynb, f)


def dumps(
    paths: list[str | Path],
    codes: list[str] | None = None,
    metadata: str | Path | None = None,
) -> str:
    """Dump files and extra code cells as jupyter notebook string.
    Files will be added as is, directories will recursively include,
    and ignore anything else.

    Args:
        paths (list[str  |  Path]): Files or directories for dumping
        codes (list[str] | None, optional): Extra code cell to append to notebook
        metadata (str | Path | None, optional): Notebook filepath to copy metadata from

    Returns:
        str: ipynb (jupyter notebook) json string
    """
    with StringIO() as sio:
        dump(sio, paths, codes, metadata)
        return sio.getvalue()
