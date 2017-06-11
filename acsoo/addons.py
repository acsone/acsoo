# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os

import click

from .main import main
from .manifest import get_installable_addons


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
@click.pass_context
def addons(ctx, addons_dirs, include, exclude):
    include = _split_set(include)
    exclude = _split_set(exclude)
    if not addons_dirs:
        addons_dirs = []
        candidate_addons_dirs = (
            os.path.join('odoo', 'addons'),
            os.path.join('odoo_addons'),
        )
        for addons_dir in candidate_addons_dirs:
            if os.path.isdir(addons_dir):
                addons_dirs.append(addons_dir)
    manifests = {}
    for addons_dir in addons_dirs:
        for addon, manifest in get_installable_addons(addons_dir).items():
            if (not include or addon in include) and addon not in exclude:
                manifests[addon] = manifest
    ctx.obj.update(dict(manifests=manifests))


main.add_command(addons)


@click.command(help="Print a comma separated list of selected addons.")
@click.pass_context
def addons_list(ctx):
    manifests = ctx.obj['manifests']
    addon_names = sorted(manifests.keys())
    click.echo(','.join(addon_names))


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
    click.echo(','.join(addon_names))


addons.add_command(addons_list_depends, 'list-depends')
