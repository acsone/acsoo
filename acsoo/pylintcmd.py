# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import logging
import os
import sys
from ConfigParser import ConfigParser

import click
import pylint.lint

from .config import AcsooConfig
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


def do_pylintcmd(load_plugins, rcfile, module, expected, pylint_options):
    if not module:
        if os.path.isdir(os.path.join('odoo', 'addons')):
            module = ['odoo']
        elif os.path.isdir(os.path.join('odoo_addons')):
            module = ['odoo_addons']
        else:
            raise click.UsageError("Please provide module or package "
                                   "to lint (--module).")
    cmd = [
        '--load-plugins', load_plugins,
        '--rcfile', rcfile,
    ] + list(pylint_options) + list(module)
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


@click.command()
@click.option('--module', '-m', metavar='module_or_package', multiple=True,
              help="Module or package to lint (default: autodetected odoo "
                   "or odoo_addons).")
@click.option('--load-plugins', metavar='PLUGINS', default='pylint_odoo',
              help="Pylint plugins to use (default: pylint_odoo).")
@click.option('--rcfile', type=click.Path(dir_okay=False, exists=True),
              default=cfg_path('pylint.cfg'),
              help="Pylint configuration file. Default is provided by acsoo.")
@click.option('--expected', '-e', 'expected', metavar='MSG-IDS',
              help="Do not fail on these messages.")
@click.argument('pylint-options', nargs=-1)
@click.pass_context
def pylintcmd(ctx, load_plugins, rcfile, module, expected, pylint_options):
    """Run pylint with reasonable defaults.

    You may pass additional
    options to pylint using '--' to separate them from
    acsoo options.

    Default options are read from the
    [pylint] section of the acsoo configuration file.
    The pylint-options key in that section can be used
    to provide default additional pylint options (one
    per line). Example configuration file:

    \b
    [pylint]
    expected=fixme:5
    pylint-options=
      --disable=all
      --enable=fixme

    The above configuration file is equivalent to:

    acsoo pylint --expected=fixme:5 -- --disable=all --enable=fixme
    """
    expected = _parse_msg_string(expected)
    default_pylint_options = (ctx.default_map or {}).\
        get('default_pylint_options', [])
    pylint_options = default_pylint_options + list(pylint_options)
    do_pylintcmd(load_plugins, rcfile, module, expected, pylint_options)


main.add_command(pylintcmd, name='pylint')


def _read_defaults(config):
    section = 'pylint'
    defaults = dict(
        module=config.getlist(
            section, 'module'),
        load_plugins=config.get(
            section, 'load-plugins', default='pylint_odoo'),
        rcfile=config.get(
            section, 'rcfile', default=cfg_path('pylint.cfg')),
        expected=config.get(
            section, 'expected', flatten=True),
        default_pylint_options=config.getlist(
            section, 'pylint-options'),
    )
    return dict(pylint=defaults)


AcsooConfig.add_default_map_reader(_read_defaults)
