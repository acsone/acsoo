# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import click

from .main import main
from .bdist_wheel import do_bdist_wheel
from .tag import do_tag
from .tag_editable_requirements import do_tag_editable_requirements


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
def release(force, src, requirement, wheel_dir):
    do_tag(force)
    do_tag_editable_requirements(force, src, requirement)
    do_bdist_wheel(src, requirement, wheel_dir)


main.add_command(release)
