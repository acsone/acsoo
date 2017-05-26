# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import re
import sys

import click

from .main import main


# from tartley/colorama
ANSI_CSI_RE = re.compile('\001?\033\\[((?:\\d|;)*)([a-zA-Z])\002?')

# from OCA/maintainer-quality-tools
LOG_START_RE = re.compile(
    r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3} \d+ (?P<loglevel>\w+) '
    r'(?P<db>\S+) (?P<logger>\S+): (?P<message>.*)$')

NON_ERROR_LEVELS = ('INFO', 'DEBUG')


def _render_errors(error_records, ignored_error_records):
    msg = []
    if ignored_error_records:
        msg.append(click.style(
            '\nerrors that did not cause failure ({}):\n'.
            format(len(ignored_error_records)),
            bold=True))
        msg.extend(ignored_error_records)
    if error_records:
        msg.append(click.style(
            '\nerrors that caused failure ({}):\n'.
            format(len(error_records)),
            bold=True))
        msg.extend(error_records)
    return ''.join(msg)


def do_checklog(filename, ignore, echo):
    ignore_regexes = [re.compile(i, re.MULTILINE) for i in ignore]

    if filename:
        logfile = open(filename, 'r')
    else:
        logfile = sys.stdin

    if echo is None and not filename:
        echo = True

    try:
        cur_rec_mo = None
        cur_rec = []
        error_records = []
        ignored_error_records = []

        def _process_cur_rec():
            # record start, process current record
            if cur_rec_mo and \
                    cur_rec_mo.group('loglevel') not in NON_ERROR_LEVELS:
                record = ''.join(cur_rec)
                for ignore_regex in ignore_regexes:
                    if ignore_regex.search(record):
                        ignored_error_records.append(record)
                        break
                else:
                    error_records.append(record)

        for line in logfile:
            if echo:
                sys.stdout.write(line)
                sys.stdout.flush()
            line = ANSI_CSI_RE.sub('', line)  # strip ANSI colors
            mo = LOG_START_RE.match(line)
            if mo:
                _process_cur_rec()
                cur_rec_mo = mo
                cur_rec = [line]
            else:
                cur_rec.append(line)
        _process_cur_rec()  # last record

        if error_records or ignored_error_records:
            msg = _render_errors(error_records, ignored_error_records)
            click.echo(msg)
        if error_records:
            raise click.ClickException("errors detected in log.")
    finally:
        if filename:
            logfile.close()


@click.command(help="Check an odoo log file for errors. When no filename is "
                    "provided, read from stdin.")
@click.option('--ignore', '-i', metavar='REGEX', multiple=True,
              help="Regular expression of log records to ignore.")
@click.option('--echo/--no-echo', default=None,
              help="Echo the input file (default when reading from stdin).")
@click.argument('filename', type=click.Path(), required=False)
def checklog(filename, ignore, echo):
    do_checklog(filename, ignore, echo)


main.add_command(checklog)
