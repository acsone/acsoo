# -*- coding: utf-8 -*-
# Copyright 2016-2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os

import click

from .main import main
from .tools import check_call, cfg_path


def do_pylint(pylint_options):
    cmd = [
        'pylint',
        '--load-plugins', 'pylint_odoo',
        '--rcfile', cfg_path('pylint.cfg'),
    ] + list(pylint_options)
    if os.path.exists('odoo'):
        cmd.append('odoo')
    elif os.path.exists('odoo_addons'):
        cmd.append('odoo_addons')
    check_call(cmd)


@click.command(help='Run pylint on odoo or odoo_addons')
@click.argument('pylint-options', nargs=-1)
def pylint(pylint_options):
    do_pylint(pylint_options)


main.add_command(pylint)
