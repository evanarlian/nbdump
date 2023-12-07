from pathlib import Path

import pytest

import nbdump


@pytest.mark.parametrize(
    "files, codes, metadata",
    [
        (["src_example"], None, None),
        (["src_example/main.py"], None, None),
        (list(Path("src_example").rglob("*.py")), None, None),
        (["src_example"], [], None),
        (["src_example"], ["!ls"], None),
        (["src_example"], ["!ls"], "tests/kaggle/default/default-notebook.ipynb"),
    ],
)
def test_no_error(files, codes, metadata):
    nbdump.dumps(files, codes, metadata)


@pytest.mark.parametrize(
    "files, codes, metadata",
    [
        ("src_example", None, None),
        (Path("src_example"), None, None),
        ("src_example/main.py", None, None),
        (["src_example"], "!ls", None),
        (["src_example"], "!ls", "missing-notebook.ipynb"),
    ],
)
def test_error(files, codes, metadata):
    with pytest.raises(Exception):
        nbdump.dumps(files, codes, metadata)
