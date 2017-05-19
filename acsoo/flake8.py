# -*- coding: utf-8 -*-
# Copyright 2016-2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import click

from .main import main
from .tools import check_call, cfg_path


def do_flake8(flake8_options):
    # flake8 __init__.py
    cmd = [
        'flake8',
        '--config', cfg_path('flake8__init__.cfg'),
    ] + list(flake8_options)
    check_call(cmd)
    # flake8
    cmd = [
        'flake8',
        '--config', cfg_path('flake8.cfg'),
    ]
    check_call(cmd)


@click.command(help='Run flake8')
@click.argument('flake8-options', nargs=-1)
def flake8(flake8_options):
    do_flake8(flake8_options)


main.add_command(flake8)
