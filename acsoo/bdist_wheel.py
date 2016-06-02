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


def do_bdist_wheel(src='src',
                   requirement='requirements.txt',
                   wheel_dir='release'):
    check_call(['pip', 'wheel', '--src', src, '-r', 'requirements.txt',
                '--wheel-dir', wheel_dir])
    # TODO 'pip wheel .' is slower and sometimes buggy because of
    #      https://github.com/pypa/pip/issues/3499
    check_call(['python', 'setup.py', 'bdist_wheel',
                '--dist-dir', wheel_dir])


@click.command()
@click.option('--src', default='src', envvar='PIP_SRC',
              type=click.Path(),
              help='Directory where editable requirements are checked out')
@click.option('-r', '--requirement', default='requirements.txt',
              type=click.File())
@click.option('-w', '--wheel-dir', default='release',
              type=click.Path())
def bdist_wheel(src, requirement, wheel_dir):
    do_bdist_wheel(src, requirement, wheel_dir)


main.add_command(bdist_wheel)
