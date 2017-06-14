# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import click

from .main import main
from .wheel import do_wheel
from .tag import do_tag


def do_release(config, force, src, requirement, wheel_dir, yes,
               no_cache_dir, no_index):
    if not yes:
        click.confirm('Tag and release version {}?'.format(config.version),
                      abort=True)
        yes = True
    do_tag(config, force, src, requirement, yes)
    do_wheel(src, requirement, wheel_dir, no_cache_dir, no_index)


@click.command(help='Perform acsoo tag, and acsoo wheel')
@click.option('-f', '--force', is_flag=True,
              help='Replace an existing tag (instead of failing)')
@click.option('--src', default='src', envvar='PIP_SRC',
              type=click.Path(file_okay=False),
              help='Directory where editable requirements are checked out')
@click.option('-r', '--requirement', default='requirements.txt',
              type=click.Path(dir_okay=False, exists=True),
              help='Requirements to build (default=requirements.txt)')
@click.option('-w', '--wheel-dir', default='release',
              type=click.Path(file_okay=False),
              help='Path where the wheels will be created (default=release')
@click.option('-y', '--yes', is_flag=True, default=False)
@click.option('--no-cache-dir', is_flag=True,
              help='Disable the pip cache')
@click.option('--no-index', is_flag=True,
              help='Ignore package index '
                   '(only looking at --find-links URLs instead)')
@click.pass_context
def release(ctx, force, src, requirement, wheel_dir, yes,
            no_cache_dir, no_index):
    do_release(ctx.obj['config'], force, src, requirement, wheel_dir, yes,
               no_cache_dir, no_index)


main.add_command(release)
