# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import click

from .main import main
from .config import config, CONFIG_FILE
from .wheel import do_wheel
from .tag import do_tag
from .tag_editable_requirements import do_tag_editable_requirements


def do_release(force, src, requirement, wheel_dir, yes,
               no_cache_dir, no_index, config_file):
    if not yes:
        click.confirm('Tag and release version {}?'.format(
            config(config_file).version), abort=True)
        yes = True
    do_tag(force, yes, config_file)
    do_tag_editable_requirements(force, src, requirement, yes, config_file)
    do_wheel(src, requirement, wheel_dir, no_cache_dir, no_index, config_file)


@click.command(help='Perform acsoo tag, acsoo tag_editable_requirements and '
                    'acsoo wheel')
@click.option('-f', '--force', is_flag=True,
              help='Replace an existing tag (instead of failing)')
@click.option('--src', default='src', envvar='PIP_SRC',
              type=click.Path(),
              help='Directory where editable requirements are checked out')
@click.option('-r', '--requirement', default='requirements.txt',
              type=click.File(),
              help='Requirements to build (default=requirements.txt)')
@click.option('-w', '--wheel-dir', default='release',
              type=click.Path(),
              help='Path where the wheels will be created (default=release')
@click.option('-y', '--yes', is_flag=True, default=False)
@click.option('--no-cache-dir', is_flag=True,
              help='Disable the pip cache')
@click.option('--no-index', is_flag=True,
              help='Ignore package index '
                   '(only looking at --find-links URLs instead)')
@click.option('-c', '--config-file', default=CONFIG_FILE, type=click.File(),
              help='Configuration file')
def release(force, src, requirement, wheel_dir, yes,
            no_cache_dir, no_index, config_file):
    do_release(force, src, requirement, wheel_dir, yes,
               no_cache_dir, no_index, config_file)


main.add_command(release)
