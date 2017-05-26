# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import logging
import os
import sys
from ConfigParser import ConfigParser

import click
import pylint.lint

from .main import main
from .tools import cmd_string, log_cmd, cfg_path


def _get_failures(linter_stats, expected):
    fails = []
    no_fails = []
    for msg, count in linter_stats['by_msg'].items():
        if not count:
            continue
        if msg in expected:
            expected_count = expected[msg]
            if expected_count is None or count == expected_count:
                no_fails.append((msg, count, expected_count))
            else:
                fails.append((msg, count, expected_count))
        else:
            fails.append((msg, count, None))
    return (sorted(fails, key=lambda i: i[0]),
            sorted(no_fails, key=lambda i: i[0]))


def _failures_to_str(fails, no_fails):
    def _r(l):
        for msg, count, expected_count in l:
            res.append('  {}: {}'.format(msg, count))
            if expected_count is not None:
                res.append(' (expected {})'.format(expected_count))
            res.append('\n')

    res = []
    if no_fails:
        res.append(click.style(
            'messages that did not cause failure:\n',
            bold=True))
        _r(no_fails)
    if fails:
        res.append(click.style(
            'messages that caused failure:\n',
            bold=True))
        _r(fails)
    return ''.join(res)


def _parse_msg_string(s):
    res = {}
    s = s or ''
    for msg in s.split(','):
        msg = msg.strip()
        if not msg:
            continue
        if ':' in msg:
            msg, count = msg.split(':', 2)
            msg = msg.strip()
            count = int(count)
            res[msg] = count
        else:
            res[msg] = None
    return res


def _consolidate_expected(rcfile, expected):
    config = ConfigParser()
    config.read([rcfile])
    res = {}
    if config.has_option('ACSOO', 'expected'):
        res.update(_parse_msg_string(config.get('ACSOO', 'expected')))
    res.update(expected)
    return res


def do_pylintcmd(load_plugins, rcfile, expected, pylint_options):
    if not pylint_options:
        if os.path.isdir(os.path.join('odoo', 'addons')):
            pylint_options = ['--', 'odoo']
        if os.path.isdir(os.path.join('odoo_addons')):
            pylint_options = ['--', 'odoo_addons']
    cmd = [
        '--load-plugins', load_plugins,
        '--rcfile', rcfile,
    ] + list(pylint_options)
    log_cmd(['pylint'] + cmd, level=logging.INFO)
    lint_res = pylint.lint.Run(cmd[:], exit=False)
    sys.stdout.flush()
    sys.stderr.flush()
    expected = _consolidate_expected(rcfile, expected)
    fails, no_fails = _get_failures(lint_res.linter.stats, expected)
    if fails or no_fails:
        msg = cmd_string(['pylint'] + cmd)
        msg += '\n'
        msg += _failures_to_str(fails, no_fails)
        click.echo('\n')
        click.echo(msg)
    if fails:
        raise click.ClickException("pylint errors detected.")


@click.command(help="Run pylint with reasonable defaults. But default it "
                    "runs on odoo or odoo_addons. You may pass additional "
                    "options to pylint using '-- options' in which case "
                    "the package to lint must be passed explicitly")
@click.option('--load-plugins', default='pylint_odoo', metavar='PLUGINS')
@click.option('--rcfile', type=click.Path(), default=cfg_path('pylint.cfg'))
@click.option('--expected', '-e', 'expected', metavar='MSG-IDS',
              help="Do not fail on these messages")
@click.argument('pylint-options', nargs=-1)
def pylintcmd(load_plugins, rcfile, expected, pylint_options):
    expected = _parse_msg_string(expected)
    do_pylintcmd(load_plugins, rcfile, expected, pylint_options)


main.add_command(pylintcmd, name='pylint')
