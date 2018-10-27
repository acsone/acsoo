# -*- coding: utf-8 -*-
# Copyright 2016-2018 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from __future__ import print_function
from contextlib import contextmanager
import logging
import os
import re
import shutil
import sys
import tempfile

import click

from .cache import Cache
from .main import main
from .tools import check_call, working_directory

_logger = logging.getLogger(__name__)


def _prepare_wheel_dir(wheel_dir):
    if os.path.exists(wheel_dir):
        _logger.debug('Removing all wheels in %s.', wheel_dir)
        with working_directory(wheel_dir):
            for f in os.listdir('.'):
                if f.endswith('.whl'):
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
                        check_call([
                            "pip",
                            "wheel",
                            "--wheel-dir",
                            tmpdir,
                            "--src",
                            src,
                            "--no-deps",
                        ] + req_line.split())
                        wheelfile = os.path.join(tmpdir, os.listdir(tmpdir)[0])
                        assert wheelfile.endswith(".whl")
                        cache.put(req_line, wheelfile)
                        shutil.move(wheelfile, wheel_dir)
                    finally:
                        shutil.rmtree(tmpdir)
                else:
                    # found in cache nothing to do
                    print(
                        "Obtained {} from acsoo wheel cache as {}".
                        format(req_line, filename),
                        file=sys.stderr,
                    )
            else:
                tmpreq.write(req_line)
                tmpreq.write("\n")
        tmpreq.flush()
        yield tmpreq


def do_wheel(src, requirement, wheel_dir, no_cache_dir, no_index, no_deps,
             exclude_project=False):
    # pip/setup.py options
    pip_opts = []
    setup_opts = []
    if no_cache_dir:
        pip_opts.append('--no-cache-dir')
        setup_opts.append('--no-cache-dir')
    if no_index:
        pip_opts.append('--no-index')
        setup_opts.append('--no-index')
    if no_deps:
        pip_opts.append('--no-deps')
    # prepare and clean wheel directory
    _prepare_wheel_dir(wheel_dir)
    # build requirements.txt
    if not no_cache_dir and no_deps:
        with _get_git_reqs_from_cache(src, requirement, wheel_dir) as tmpreq:
            check_call(['pip', 'wheel', '--src', src,
                        '-r', tmpreq.name,
                        '--wheel-dir', wheel_dir] + pip_opts)
    else:
        check_call(['pip', 'wheel', '--src', src, '-r', requirement.name,
                    '--wheel-dir', wheel_dir] + pip_opts)
    # build project
    if not exclude_project:
        # TODO 'pip wheel .' is slower and sometimes buggy because of
        #      https://github.com/pypa/pip/issues/3499
        if os.path.exists('build'):
            shutil.rmtree('build')
        check_call(['python', 'setup.py', 'bdist_wheel',
                    '--dist-dir', wheel_dir] + setup_opts)


@click.command(help='Build wheels for all dependencies found in '
                    'requirements.txt, plus the project in the current '
                    'directory. CAUTION: all wheel files are removed from '
                    'the target directory before building')
@click.option('--src', default='src', envvar='PIP_SRC',
              type=click.Path(file_okay=False),
              help='Directory where editable requirements are checked out')
@click.option('-r', '--requirement', default='requirements.txt',
              type=click.File(),
              help='Requirements to build (default=requirements.txt)')
@click.option('-w', '--wheel-dir', default='release',
              type=click.Path(file_okay=False),
              help='Path where the wheels will be created (default=release')
@click.option('--no-cache-dir', is_flag=True,
              help='Disable the pip cache')
@click.option('--no-index', is_flag=True,
              help='Ignore package index '
                   '(only looking at --find-links URLs instead)')
@click.option('--no-deps', is_flag=True,
              help='Don\'t look for package dependencies.')
@click.option('--exclude-project', is_flag=True,
              help='Do not build current project')
def wheel(src, requirement, wheel_dir, no_cache_dir, no_index, no_deps,
          exclude_project=False):
    do_wheel(src, requirement, wheel_dir, no_cache_dir, no_index, no_deps,
             exclude_project)


main.add_command(wheel)
