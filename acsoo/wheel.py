# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import logging
import re
import os

import click

from .main import main
from .config import config
from .tools import check_call, working_directory

_logger = logging.getLogger(__name__)


def do_wheel(src, requirement, wheel_dir):
    if os.path.exists(wheel_dir):
        _logger.debug('Removing all wheels in %s.', wheel_dir)
        with working_directory(wheel_dir):
            for f in os.listdir('.'):
                if f.endswith('.whl'):
                    os.remove(f)
    check_call(['pip', 'wheel', '--src', src, '-r', 'requirements.txt',
                '--wheel-dir', wheel_dir])
    # TODO 'pip wheel .' is slower and sometimes buggy because of
    #      https://github.com/pypa/pip/issues/3499
    check_call(['python', 'setup.py', 'bdist_wheel',
                '--dist-dir', wheel_dir])


@click.command(help='Build wheels for all dependencies found in '
                    'requirements.txt, plus the project in the current '
                    'directory. CAUTION: all wheel files are removed from '
                    'the target directory before building')
@click.option('--src', default='src', envvar='PIP_SRC',
              type=click.Path(),
              help='Directory where editable requirements are checked out')
@click.option('-r', '--requirement', default='requirements.txt',
              type=click.File(),
              help='Requirements to build (default=requirements.txt)')
@click.option('-w', '--wheel-dir', default='release',
              type=click.Path(),
              help='Path where the wheels will be created (default=release')
def wheel(src, requirement, wheel_dir):
    do_wheel(src, requirement, wheel_dir)


main.add_command(wheel)
