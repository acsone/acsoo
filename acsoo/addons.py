# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os

import click

from .main import main
from .manifest import get_installable_addons


@click.group(help='Do things with addons lists')
@click.option('--addons-dir', 'addons_dirs', multiple=True, type=click.Path(),
              help="Directory containing addons. Defaults to odoo/addons or "
                   "odoo_addons if present. This option can be repeated.")
@click.pass_context
def addons(ctx, addons_dirs):
    manifests = {}
    if not addons_dirs:
        addons_dirs = []
        candidate_addons_dirs = (
            os.path.join('odoo', 'addons'),
            os.path.join('odoo_addons'),
        )
        for addons_dir in candidate_addons_dirs:
            if os.path.exists(addons_dir):
                addons_dirs.append(addons_dir)
    for addons_dir in addons_dirs:
        manifests.update(get_installable_addons(addons_dir))
    ctx.obj = dict(manifests=manifests)


main.add_command(addons)


@click.command(help="Print a comma separated list of the installable addons "
                    "found in --addons-dir.")
@click.pass_context
def addons_list(ctx):
    manifests = ctx.obj['manifests']
    addon_names = sorted(manifests.keys())
    click.echo(','.join(addon_names))


addons.add_command(addons_list, 'list')


@click.command(help="Print a comma separated list of the direct dependencies "
                    "of installable addons found in --addons-dir.")
@click.pass_context
def addons_depends(ctx):
    manifests = ctx.obj['manifests']
    depends = set()
    for manifest in manifests.values():
        depends.update(manifest.get('depends', []))
    depends -= set(manifests.keys())
    addon_names = sorted(depends)
    click.echo(','.join(addon_names))


addons.add_command(addons_depends, 'depends')
