# -*- coding: utf-8 -*-
# Copyright 2016-2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import subprocess

import click

from .main import main


def do_lint(exclude):
    r = 0
    # flake8
    cmd = ['flake8']
    if exclude:
        cmd.extend(['--exclude', exclude])
    r += subprocess.call(cmd)
    # pylint
    # TODO
    return r


@click.command(help='Lint Odoo code, using flake8 and pylint(-odoo)')
@click.option('--exclude', default='src',
              type=click.Path(),
              help='Excluded directories')
def lint(exclude):
    r = do_lint(exclude)
    if r != 0:
        raise SystemExit(r)


main.add_command(lint)
