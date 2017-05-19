# -*- coding: utf-8 -*-
# Copyright 2016-2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import logging

import click

from .main import main
from .tools import call, cfg_path


def do_lint(flake8_append_config):
    r = 0
    # flake8 __init__.py
    cmd = [
        'flake8',
        '--config', cfg_path('flake8__init__.cfg'),
    ]
    r += call(cmd, log_level=logging.INFO)
    # flake8
    cmd = [
        'flake8',
        '--config', cfg_path('flake8.cfg'),
    ]
    if flake8_append_config:
        cmd.extend(['--append-config', flake8_append_config])
    r += call(cmd, log_level=logging.INFO)
    # pylint
    # TODO
    return r


@click.command(help='Lint Odoo code, using flake8 and pylint(-odoo)')
@click.option('--flake8-append-config',
              type=click.Path())
def lint(flake8_append_config):
    r = do_lint(flake8_append_config)
    if r != 0:
        raise click.ClickException("acsoo lint errors")


main.add_command(lint)
