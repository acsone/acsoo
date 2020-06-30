# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import re
from typing import Iterable, Optional

import click

from .main import main
from .tools import check_output, find_python

_EQUAL_RE = re.compile(r"^([A-Za-z0-9-_.]+)\s*[@=]")
_EGG_RE = re.compile(r"egg=([A-Za-z0-9-_.]+)")


def _canonicalize(distribution: str) -> str:
    """Canonicalize a distribution name"""
    return distribution.lower().replace("_", "-")


def _req_dist(req: str) -> Optional[str]:
    """Find a distribution name in a pip requirement line"""
    mo = _EQUAL_RE.search(req) or _EGG_RE.search(req)
    if mo:
        return _canonicalize(mo.group(1))
    return None


def _list_depends(distribution: str, python: str) -> Iterable[str]:
    """Obtain transitive dependencies of a distributions"""
    _list_depends = os.path.join(os.path.dirname(__file__), "_list_depends")
    cmd = [find_python(python), _list_depends, distribution]
    dependencies = check_output(cmd).strip().split("\n")
    return {_canonicalize(d) for d in dependencies}


def _pip_freeze(python: str) -> Iterable[str]:
    cmd = [find_python(python), "-m", "pip", "freeze"]
    frozen = check_output(cmd).strip().split("\n")
    return frozen


def _freeze(distribution: str, python: str) -> Iterable[str]:
    # get dependencies
    dependencies = _list_depends(distribution, python)
    # call regular pip freeze
    frozen = _pip_freeze(python)
    # filter out pip freeze lines that are not in dependencies
    for req in frozen:
        req_dist = _req_dist(req)
        if req_dist and req_dist not in dependencies:
            continue
        yield req


@click.command()
@click.argument("distribution")
@click.option("--python", "-p", default="python")
def freeze(distribution: str, python: str) -> None:
    """pip freeze, but output only dependencies of a given distribution."""
    for req in _freeze(distribution, python):
        print(req)


main.add_command(freeze)
