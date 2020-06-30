import subprocess
import sys
from pathlib import Path

import pytest

from acsoo.freeze import _freeze

DATA_DIR = Path(__file__).parent / "data"

# pkga: no dependencies
# pkgb: depends on pkga


@pytest.mark.parametrize(
    "to_install, distribution, expected",
    [
        (["pkga"], "pkga", []),
        (["pkgb"], "pkgb", ["pkga==0.0.0"]),
        (["pkgb"], "pkga", []),
    ],
)
def test_freeze(to_install, distribution, expected, tmp_path):
    subprocess.check_call(["virtualenv", "-p", sys.executable, tmp_path / "venv"])
    subprocess.check_call(
        [
            tmp_path / "venv" / "bin" / "pip",
            "install",
            "-f",
            DATA_DIR / "freezetestpkgs",
        ]
        + to_install
    )
    assert (
        list(_freeze(distribution, str(tmp_path / "venv" / "bin" / "python")))
        == expected
    )
