# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import click

from .main import main
from .config import config
from .tools import check_call, call, check_output


def do_tag(force):
    if force:
        force_cmd = ['-f']
    else:
        force_cmd = []
    if 0 != call(['git', 'diff', '--exit-code']):
        raise RuntimeError("please commit first")
    if 0 != call(['git', 'diff', '--exit-code', '--cached']):
        raise RuntimeError("please commit first")
    if check_output(['git', 'ls-files', '--other', '--exclude-standard',
                     '--directory']):
        raise RuntimeError("please commit first")
    check_call(['git', 'tag'] + force_cmd +
               [config().version])
    check_call(['git', 'push'] + force_cmd +
               ['origin', 'tag', config().version])


@click.command(help='Tag the current project after ensuring '
                    'everything has been commited to git.')
@click.option('-f', '--force', is_flag=True,
              help='Replace an existing tag (instead of failing)')
def tag(force):
    do_tag(force)


main.add_command(tag)
