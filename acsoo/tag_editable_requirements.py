# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import logging
import re
import os

import click

from .main import main
from .config import config
from .tools import check_call, working_directory

_logger = logging.getLogger(__name__)


RE = re.compile(r"^-e git\+(?P<url>ssh://.*?/.*?)@(?P<sha>[^?#&]+)"
                r".*?[#?]egg=(?P<egg>[^?#&]+)")


def do_tag_editable_requirements(force, src, requirement, yes):
    tag = '{}-{}_{}'.format(
        config().series, config().trigram, config().version)
    if not yes:
        click.confirm('Tag dependencies with {}?'.format(tag), abort=True)
    if force:
        force_cmd = ['-f']
    else:
        force_cmd = []
    for req in requirement:
        req = req.strip()
        mo = RE.match(req)
        if not mo:
            continue
        url = mo.group('url')
        sha = mo.group('sha')
        egg = mo.group('egg')
        repo = os.path.join(src, egg.replace('_', '-'))
        if not os.path.isdir(os.path.join(repo, '.git')):
            raise click.ClickException('{} is not a git repository.'.
                                       format(repo))

        with working_directory(repo):
            _logger.info('placing tag %s on %s@%s', tag, url, sha)
            check_call(['git', 'fetch', url, sha])
            check_call(['git', 'tag'] + force_cmd + [tag, sha])
            check_call(['git', 'push'] + force_cmd + [url, tag])


@click.command(help='Tag all editable requirements found in '
                    'requirements.txt, so the commits referenced in '
                    'there are not lost in case of git garbage collection.')
@click.option('-f', '--force', is_flag=True,
              help='Replace an existing tag (instead of failing)')
@click.option('--src', default='src', envvar='PIP_SRC',
              type=click.Path(),
              help='Directory where editable requirements are checked out')
@click.option('-r', '--requirement', default='requirements.txt',
              type=click.File(),
              help='Requirements to build (default=requirements.txt)')
@click.option('-y', '--yes', is_flag=True, default=False)
def tag_editable_requirements(force, src, requirement, yes):
    do_tag_editable_requirements(force, src, requirement, yes)


main.add_command(tag_editable_requirements)
