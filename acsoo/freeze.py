# -*- coding: utf-8 -*-
# Copyright 2020 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import re

import click

from .main import main
from .tools import check_output, find_python

_EQUAL_RE = re.compile(r"^([A-Za-z-_.]+)\s*[@=]")
_EGG_RE = re.compile(r"egg=([A-Za-z-_.]+)")


def _canonicalize(distribution):
    """Canonicalize a distribution name"""
    return distribution.lower().replace("_", "-")


def _req_dist(req):
    """Find a distribution name in a pip requirement line"""
    mo = _EQUAL_RE.search(req) or _EGG_RE.search(req)
    if mo:
        return _canonicalize(mo.group(1))
    return None


def _get_dependencies(distribution, python):
    """Obtain transitive dependencies of a distributions"""
    _list_depends = os.path.join(os.path.dirname(__file__), "_list_depends")
    cmd = [find_python(python), _list_depends, distribution]
    dependencies = check_output(cmd).strip().split("\n")
    return {_canonicalize(d) for d in dependencies}


def _freeze(python):
    cmd = [find_python(python), "-m", "pip", "freeze"]
    frozen = check_output(cmd).strip().split("\n")
    return frozen


@click.command()
@click.argument("distribution")
@click.option("--python", "-p", default="python")
def freeze(distribution, python):
    """pip freeze, but output only dependencies of a given distribution."""
    # get dependencies
    dependencies = _get_dependencies(distribution, python)
    # call regular pip freeze
    frozen = _freeze(python)
    # filter out pip freeze lines that are not in dependencies
    for req in frozen:
        req_dist = _req_dist(req)
        if req_dist and req_dist not in dependencies:
            continue
        print(req)


main.add_command(freeze)
