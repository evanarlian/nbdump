import toml
from packaging import version

from nbdump import __version__


def test_versions_match():
    with open("pyproject.toml", "r") as f:
        ver = toml.load(f)["project"]["version"]
    assert version.parse(ver) == version.parse(__version__)
