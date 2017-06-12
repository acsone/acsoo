# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import click

from .main import main
from .tools import check_call, call, check_output
from .tag_requirements import do_tag_requirements


def do_tag(config, force, src, requirement, yes):
    tag = config.version
    if not yes:
        click.confirm('Tag project with {}?'.format(tag), abort=True)
    if force:
        force_cmd = ['-f']
    else:
        force_cmd = []
    if call(['git', 'diff', '--exit-code']) != 0:
        raise click.ClickException("Please commit first.")
    if call(['git', 'diff', '--exit-code', '--cached']) != 0:
        raise click.ClickException("Please commit first.")
    out = check_output(['git', 'ls-files', '--other', '--exclude-standard',
                        '--directory'])
    if out:
        click.echo(out)
        raise click.ClickException("Please commit first.")
    check_call(['git', 'tag'] + force_cmd + [tag])
    check_call(['git', 'push', '-q'] + force_cmd + ['origin', 'tag', tag])
    do_tag_requirements(config, force, src, requirement, yes)


@click.command(help='Tag the current project after ensuring '
                    'everything has been commited to git.')
@click.option('--src', default='src', envvar='PIP_SRC',
              type=click.Path(file_okay=False),
              help='Directory where editable requirements are checked out')
@click.option('-r', '--requirement', default='requirements.txt',
              type=click.Path(dir_okay=False, exists=True),
              help='Requirements to build (default=requirements.txt)')
@click.option('-f', '--force', is_flag=True,
              help='Replace an existing tag (instead of failing)')
@click.option('-y', '--yes', is_flag=True, default=False)
@click.pass_context
def tag(ctx, force, src, requirement, yes):
    """ Tag the current project and its VCS requirements.

    This command verifies everything has been committed, then
    performs git tag, git push and acsoo tag_requirements.
    """
    do_tag(ctx.obj['config'], force, src, requirement, yes)


main.add_command(tag)
