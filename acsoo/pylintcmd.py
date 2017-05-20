# -*- coding: utf-8 -*-
# Copyright 2016-2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import logging
import os
import sys
from ConfigParser import ConfigParser

import click
import pylint.lint

from .main import main
from .tools import cmd_string, log_cmd, cfg_path


def _get_failures(linter_stats, no_fail):
    fails = []
    no_fails = []
    for msg, count in linter_stats['by_msg'].items():
        if not count:
            continue
        if msg in no_fail:
            no_fails.append((msg, count))
        else:
            fails.append((msg, count))
    return (sorted(fails, key=lambda i: i[1]),
            sorted(no_fails, key=lambda i: i[1]))


def _parse_cs_string(s):
    """Parse a comma-separated string and return a list."""
    s = s and s.strip()
    if not s:
        return []
    else:
        return [part.strip() for part in s.split(',')]


def _consolidate_no_fail(rcfile, no_fail, fail):
    config = ConfigParser()
    config.read([rcfile])
    res = set()
    if config.has_option('ACSOO', 'no-fail'):
        res.update(_parse_cs_string(config.get('ACSOO', 'no-fail')))
    res.update(no_fail)
    return res - set(fail)


def do_pylintcmd(load_plugins, rcfile, no_fail, fail, pylint_options):
    cmd = [
        '--load-plugins', load_plugins,
        '--rcfile', rcfile,
    ] + list(pylint_options)
    if os.path.exists('odoo'):
        cmd.append('odoo')
    elif os.path.exists('odoo_addons'):
        cmd.append('odoo_addons')
    log_cmd(['pylint'] + cmd, level=logging.INFO)
    lint_res = pylint.lint.Run(cmd[:], exit=False)
    sys.stdout.flush()
    sys.stderr.flush()
    no_fail = _consolidate_no_fail(rcfile, no_fail, fail)
    fails, no_fails = _get_failures(lint_res.linter.stats, no_fail)
    if fails:
        msg = cmd_string(['pylint'] + cmd)
        msg += '\n  messages that caused failure:\n    '
        msg += '\n    '.join(['{0}: {1}'.format(*i) for i in fails])
        if no_fails:
            msg += '\n  messages that did not cause failure:\n    '
            msg += '\n    '.join(['{0}: {1}'.format(*i) for i in no_fails])
        raise click.ClickException(msg)


@click.command(help='Run pylint on odoo or odoo_addons')
@click.option('--load-plugins', default='pylint_odoo', metavar='PLUGINS')
@click.option('--rcfile', type=click.Path(), default=cfg_path('pylint.cfg'))
@click.option('--no-fail', 'no_fail', metavar='MSG-IDS',
              help="Do not fail on these messages")
@click.option('--fail', 'fail', metavar='MSG-IDS',
              help="Fail on these messages even if they are in no-fail")
@click.argument('pylint-options', nargs=-1)
def pylintcmd(load_plugins, rcfile, no_fail, fail, pylint_options):
    no_fail = _parse_cs_string(no_fail)
    fail = _parse_cs_string(fail)
    do_pylintcmd(load_plugins, rcfile, no_fail, fail, pylint_options)


main.add_command(pylintcmd, name='pylint')
