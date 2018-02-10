# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from configparser import ConfigParser
import os
import subprocess
import sys

import click

from .main import main


OPTIONS = [
    ('db_host', 'PGHOST'),
    ('db_port', 'PGPORT'),
    ('db_user', 'PGUSER'),
    ('db_password', 'PGPASSWORD'),
    ('db_name', 'PGDATABASE'),
]


def _get_option(config, option):
    section = 'options'
    if not config.has_option(section, option):
        return None
    value = config.get(section, option)
    if value in ('False', 'false'):
        return False
    return value


def pgenv_from_odoo_config(odoo_config):
    """
    Return a dictionary of postgres environment
    variables from an Odoo configuration file.
    Variables set to False, false or absent from the Odoo
    configuration are absent in the dictionary.
    """
    parsed_odoo_config = ConfigParser()
    parsed_odoo_config.readfp(odoo_config)
    res = {}
    for option, pgvar in OPTIONS:
        value = _get_option(parsed_odoo_config, option)
        if value not in (None, False):
            res[pgvar] = value
    return res


def echo_posix_pgenv(pgenv):
    for __, key in OPTIONS:
        if key in pgenv:
            value = pgenv[key]
            value = value.replace('"', '\\"')
            click.echo('{key}="{value}"; export {key}'.format(**locals()))


@click.group(invoke_without_command=True)
@click.option('--odoo-config', '-c', type=click.File(),
              required=True, envvar=['OPENERP_SERVER', 'ODOO_RC'],
              help="Odoo configuration file (can also be set in "
                   "ODOO_RC or OPENERP_SERVER environment variables).")
@click.pass_context
def pgenv(ctx, odoo_config):
    """Do things with the postgres environment read from an
    Odoo configuration file. The default behaviour without
    subcommand is the same as running the 'posix' subcommand.
    """
    pgenv = pgenv_from_odoo_config(odoo_config)
    if not ctx.invoked_subcommand:
        echo_posix_pgenv(pgenv)
    else:
        ctx.obj['pgenv'] = pgenv


main.add_command(pgenv, name='pgenv')


@click.command()
@click.pass_context
def posix(ctx):
    """Print postgres environment variables in a format
    that can be evaluated by a POSIX shell. For instance,
    'eval $(acsoo pgenv -c odoo.cfg)' will set the environment
    variables in bash.
    """
    pgenv = ctx.obj['pgenv']
    echo_posix_pgenv(pgenv)


pgenv.add_command(posix)


@click.command()
@click.argument('cmd', nargs=-1, required=True)
@click.pass_context
def exec_cmd(ctx, cmd):
    """Execute a command with the postgres environment variables
    set. Example: 'acsoo pgenv -c odoo.cfg exec psql'.
    """
    pgenv = ctx.obj['pgenv']
    env = os.environ.copy()
    env.update(pgenv)
    r = subprocess.call(cmd, env=env)
    sys.exit(r)


pgenv.add_command(exec_cmd, 'exec')
