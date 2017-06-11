# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import logging
import os
import shutil

import click

from .main import main
from .tools import check_call, working_directory

_logger = logging.getLogger(__name__)


def do_wheel(src, requirement, wheel_dir, no_cache_dir, no_index):
    if os.path.exists(wheel_dir):
        _logger.debug('Removing all wheels in %s.', wheel_dir)
        with working_directory(wheel_dir):
            for f in os.listdir('.'):
                if f.endswith('.whl'):
                    os.remove(f)
    opts = []
    if no_cache_dir:
        opts.append('--no-cache-dir')
    if no_index:
        opts.append('--no-index')
    check_call(['pip', 'wheel', '--src', src, '-r', 'requirements.txt',
                '--wheel-dir', wheel_dir] + opts)
    # TODO 'pip wheel .' is slower and sometimes buggy because of
    #      https://github.com/pypa/pip/issues/3499
    if os.path.exists('build'):
        shutil.rmtree('build')
    check_call(['python', 'setup.py', 'bdist_wheel',
                '--dist-dir', wheel_dir] + opts)


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
def wheel(src, requirement, wheel_dir, no_cache_dir, no_index):
    do_wheel(src, requirement, wheel_dir, no_cache_dir, no_index)


main.add_command(wheel)
