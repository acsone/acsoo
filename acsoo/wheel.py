# -*- coding: utf-8 -*-
# Copyright 2016-2018 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from __future__ import print_function

import logging
import os
import re
import shutil
import sys
import tempfile
from contextlib import contextmanager

import click

from .cache import Cache
from .main import main
from .tools import check_call, working_directory

_logger = logging.getLogger(__name__)


def _prepare_wheel_dir(wheel_dir):
    if os.path.exists(wheel_dir):
        _logger.debug("Removing all wheels in %s.", wheel_dir)
        with working_directory(wheel_dir):
            for f in os.listdir("."):
                if f.endswith(".whl"):
                    os.remove(f)
    else:
        os.makedirs(wheel_dir)


@contextmanager
def _get_git_reqs_from_cache(src, requirement, wheel_dir):
    """ Parse a requirement file and fetch git references from cache.

    Yield a temporary requirement file where git references
    that could be fetched from cache are removed.
    """
    GITREF_RE = re.compile("^-e git.*?@([a-f0-9]{40}).*egg=(?P<egg>[^#& ]+)")
    cache = Cache("acsoo-wheel")
    with tempfile.NamedTemporaryFile(mode="w") as tmpreq:
        for req_line in requirement:
            req_line = req_line.strip()
            mo = GITREF_RE.match(req_line)
            if mo:
                filename = cache.get(req_line, wheel_dir)
                if not filename:
                    # not found in cache
                    tmpdir = tempfile.mkdtemp()
                    try:
                        check_call(
                            [
                                "pip",
                                "wheel",
                                "--wheel-dir",
                                tmpdir,
                                "--src",
                                src,
                                "--no-deps",
                            ]
                            + req_line.split()
                        )
                        wheelfile = os.path.join(tmpdir, os.listdir(tmpdir)[0])
                        assert wheelfile.endswith(".whl")
                        cache.put(req_line, wheelfile)
                        shutil.move(wheelfile, wheel_dir)
                    finally:
                        shutil.rmtree(tmpdir)
                else:
                    # found in cache nothing to do
                    print(
                        "Obtained {} from acsoo wheel cache as {}".format(
                            req_line, filename
                        ),
                        file=sys.stderr,
                    )
            else:
                tmpreq.write(req_line)
                tmpreq.write("\n")
        tmpreq.flush()
        yield tmpreq


def do_wheel(
    src, requirement, wheel_dir, no_cache_dir, no_index, no_deps, exclude_project=False
):
    # pip/setup.py options
    pip_cmd = ["pip", "wheel", "--src", src, "--wheel-dir", wheel_dir]
    if no_cache_dir:
        pip_cmd.append("--no-cache-dir")
    if no_index:
        pip_cmd.append("--no-index")
    if no_deps:
        pip_cmd.append("--no-deps")
    if not exclude_project:
        pip_cmd.extend(["-e", "."])
    # prepare and clean wheel directory
    _prepare_wheel_dir(wheel_dir)
    # pip wheel
    if not no_cache_dir and no_deps:
        with _get_git_reqs_from_cache(src, requirement, wheel_dir) as tmpreq:
            check_call(pip_cmd + ["-r", tmpreq.name])
    else:
        check_call(pip_cmd + ["-r", requirement.name])


@click.command()
@click.option(
    "--src",
    default="src",
    envvar="PIP_SRC",
    type=click.Path(file_okay=False),
    show_default=True,
    help="Directory where editable requirements are checked out",
)
@click.option(
    "-r",
    "--requirement",
    default="requirements.txt",
    type=click.File(),
    show_default=True,
    help="Requirements to build",
)
@click.option(
    "-w",
    "--wheel-dir",
    default="release",
    type=click.Path(file_okay=False),
    show_default=True,
    help="Path where the wheels will be created",
)
@click.option("--no-cache-dir", is_flag=True, help="Disable the pip cache")
@click.option(
    "--no-index",
    is_flag=True,
    help="Ignore package index " "(only looking at --find-links URLs instead)",
)
@click.option("--no-deps", is_flag=True, help="Don't look for package dependencies.")
@click.option("--exclude-project", is_flag=True, help="Do not build current project")
def wheel(
    src, requirement, wheel_dir, no_cache_dir, no_index, no_deps, exclude_project=False
):
    """Build wheels for all dependencies found in requirements.txt,
    plus the project in the current directory.

    The main advantage of this command (compared to a regular
    `pip wheel -r requirements.txt -e . --wheel_dir=release --src src`),
    is that it maintains a cache of git dependencies that are pinned with
    a sha1.

    CAUTION: all wheel files are removed from the target directory before
    building.
    """
    do_wheel(
        src, requirement, wheel_dir, no_cache_dir, no_index, no_deps, exclude_project
    )


main.add_command(wheel)
