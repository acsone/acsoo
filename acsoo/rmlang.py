# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import click

from .main import main
from .tools import check_call, check_output


def do_rmlang(keep):
    keeps = [l + '.po' for l in keep.split(',')]
    toremove = []
    filenames = check_output(['git', 'ls-files', '-z', '*.po'])
    for filename in filenames.split('\x00'):
        if not filename:
            continue
        for keep in keeps:
            if filename.endswith(keep):
                break
        else:
            toremove.append(filename)
    if toremove:
        check_call(['git', 'rm'] + toremove)


@click.command(help='Remove .po files except the listed languages.')
@click.option('-k', '--keep', required=True,
              help='Comma separated list of languages to keep.')
def rmlang(keep):
    do_rmlang(keep)


main.add_command(rmlang)
