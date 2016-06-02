# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import click

from .main import main
from .config import config
from .bdist_wheel import do_bdist_wheel
from .tag import do_tag
from .tag_editable_requirements import do_tag_editable_requirements


def do_release(force, src, requirement, wheel_dir, yes):
    if not yes:
        click.confirm('Tag and release version {}?'.format(config().version),
                      abort=True)
        yes = True
    do_tag(force, yes)
    do_tag_editable_requirements(force, src, requirement, yes)
    do_bdist_wheel(src, requirement, wheel_dir)


@click.command(help='Perform tag, tag_editable_requirements and bdist_wheel')
@click.option('-f', '--force', is_flag=True,
              help='Replace an existing tag (instead of failing)')
@click.option('--src', default='src', envvar='PIP_SRC',
              type=click.Path(),
              help='Directory where editable requirements are checked out')
@click.option('-r', '--requirement', default='requirements.txt',
              type=click.File())
@click.option('-w', '--wheel-dir', default='release',
              type=click.Path())
@click.option('-y', '--yes', is_flag=True, default=False)
def release(force, src, requirement, wheel_dir, yes):
    do_release(force, src, requirement, wheel_dir, yes)


main.add_command(release)
