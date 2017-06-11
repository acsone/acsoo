# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import logging

import click

from .config import AcsooConfig
from .main import main
from .tools import check_call, cfg_path


def do_flake8(config, flake8_options):
    # flake8 __init__.py
    cmd = [
        'flake8',
        '--config', cfg_path('flake8__init__.cfg'),
    ]
    check_call(cmd, log_level=logging.INFO)
    # flake8
    cmd = [
        'flake8',
        '--config', config,
    ] + list(flake8_options)
    check_call(cmd, log_level=logging.INFO)


@click.command()
@click.option('--config', type=click.Path(dir_okay=False, exists=True),
              default=cfg_path('flake8.cfg'),
              help="Flake8 config file. Default is provided by acsoo.")
@click.argument('flake8-options', nargs=-1)
@click.pass_context
def flake8(ctx, config, flake8_options):
    """Run flake8 with reasonable defaults.

    You may pass additional
    options to flake8 using '--' to separate them from
    acsoo options.

    Default options are read from the
    [flake8] section of the acsoo configuration file.
    The flake8-options key in that section can be used
    to provide default additional flake8 options (one
    per line). Example configuration file:

    \b
    [flake8]
    pylint-options=
      --append-config=flake8.cfg

    The above configuration file is equivalent to:

    acsoo flake8 -- --append-config=flake8.cfg
    """
    default_flake8_options = (ctx.default_map or {}).\
        get('default_flake8_options', [])
    flake8_options = default_flake8_options + list(flake8_options)
    do_flake8(config, flake8_options)


main.add_command(flake8)


def _read_defaults(config):
    section = 'flake8'
    defaults = dict(
        config=config.get(
            section, 'config', default=cfg_path('flake8.cfg')),
        default_flake8_options=config.getlist(
            section, 'flake8-options'),
    )
    return dict(flake8=defaults)


AcsooConfig.add_default_map_reader(_read_defaults)
