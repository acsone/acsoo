# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os

import click

from .main import main
from .manifest import get_installable_addons
from .tools import check_output


def _split_set(csv):
    return set(s.strip() for s in csv.split(',') if s.strip())


@click.group(help="Do things with addons lists. Options of this command "
                  "select addons on which the subcommands will act.")
@click.option('--addons-dir', 'addons_dirs', multiple=True,
              type=click.Path(file_okay=False, exists=True),
              help="Directory containing addons. Defaults to odoo/addons or "
                   "odoo_addons if present. This option can be repeated.")
@click.option('--include', default='',
              help="Comma separated list of addons to include (default: all "
                   "installable addons found in --addons-dir').")
@click.option('--exclude', default='',
              help="Comma separated list of addons to exclude.")
@click.option('--separator', '-s', default=',',
              help="Separator (default: comma)")
@click.pass_context
def addons(ctx, addons_dirs, include, exclude, separator):
    include = _split_set(include)
    exclude = _split_set(exclude)
    if not addons_dirs:
        addons_dirs = []
        candidate_addons_dirs = (
            os.path.join('odoo', 'addons'),
            'odoo_addons',
            '.',
        )
        for addons_dir in candidate_addons_dirs:
            if os.path.isdir(addons_dir):
                addons_dirs.append(addons_dir)
    manifests = {}
    for addons_dir in addons_dirs:
        for addon, manifest in get_installable_addons(addons_dir).items():
            if (not include or addon in include) and addon not in exclude:
                manifests[addon] = manifest
    ctx.obj.update(dict(
        manifests=manifests,
        separator=separator,
        addons_dirs=addons_dirs,
    ))


main.add_command(addons)


@click.command(help="Print a comma separated list of selected addons.")
@click.pass_context
def addons_list(ctx):
    manifests = ctx.obj['manifests']
    addon_names = sorted(manifests.keys())
    click.echo(ctx.obj['separator'].join(addon_names))


addons.add_command(addons_list, 'list')


@click.command(help="Print a comma separated list of the direct dependencies "
                    "of installable addons found in --addons-dir.")
@click.option('--exclude', default='',
              help="Comma separated list of addons to exclude from "
                   "the dependencies.")
@click.pass_context
def addons_list_depends(ctx, exclude):
    exclude = _split_set(exclude)
    manifests = ctx.obj['manifests']
    depends = set()
    for manifest in manifests.values():
        depends.update(manifest.get('depends', []))
    depends -= set(manifests.keys())
    depends -= exclude
    addon_names = sorted(depends)
    click.echo(ctx.obj['separator'].join(addon_names))


addons.add_command(addons_list_depends, 'list-depends')


@click.command(help="Print a coma separated list of the modified addons "
                    "against the specifiec target branch.")
@click.argument('branch', default='origin/master...')
@click.option('--exclude', default='',
              help="Comma separated list of addons to exclude from the "
                   "modified addons.")
@click.pass_context
def addons_diff(ctx, branch, exclude):
    exclude = _split_set(exclude)
    manifests = ctx.obj['manifests']
    addon_names = sorted(manifests.keys())
    cmd = [
        "git",
        "diff",
        "--name-only",
        branch,
    ]
    diff_files = check_output(cmd).split('\n')[0:-1]
    diff_addons = set()
    addons_dirs = ctx.obj.get('addons_dirs', [])
    exclude |= set(addons_dirs)
    for addons_dir in addons_dirs:
        for diff_file in diff_files:
            diff_path = diff_file.replace(
                "{addons_dir}/".format(addons_dir=addons_dir), "")
            diff_addon = diff_path.split('/')[0]
            if diff_addon not in exclude and diff_addon in addon_names:
                diff_addons.add(diff_addon)
    diff_addons = sorted(diff_addons)
    click.echo(ctx.obj['separator'].join(diff_addons))


addons.add_command(addons_diff, 'list-diff')
