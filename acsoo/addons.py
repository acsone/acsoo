# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import re

import click

from .main import main
from .manifest import get_default_addons_dirs, get_installable_addons
from .tools import call, check_output, parse_requirements


ODOO_ADDON_REGEX = re.compile(
    r'odoo[0-9]+[-_]addon[-_].*'
)
EXTERNAL_SOURCES_REGEX = re.compile(
    r'odoo[-_]addons[-_].*'
)


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
    addons = {}
    installable_addons = get_installable_addons(addons_dirs)
    for addon_name, (addon_dir, manifest) in installable_addons.items():
        if (not include or addon_name in include) and \
                addon_name not in exclude:
            addons[addon_name] = (addon_dir, manifest)
    ctx.obj.update(dict(
        addons=addons,
        separator=separator,
    ))


main.add_command(addons)


@click.command(help="Print a comma separated list of selected addons.")
@click.pass_context
def addons_list(ctx):
    addons = ctx.obj['addons']
    addon_names = sorted(addons.keys())
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
    addons = ctx.obj['addons']
    depends = set()
    for addon_dir, manifest in addons.values():
        depends.update(manifest.get('depends', []))
    depends -= set(addons.keys())
    depends -= exclude
    addon_names = sorted(depends)
    click.echo(ctx.obj['separator'].join(addon_names))


addons.add_command(addons_list_depends, 'list-depends')


@click.command(help="Print a comma separated list of the modified installable "
                    "addons from the given git ref")
@click.argument('git_ref')
@click.option('-d', '--tmp-dir', 'tmp_dir', default='tmp_acsoo_toupdate',
              type=click.Path(file_okay=False),
              help='Path where the repository will be cloned for comparison')
@click.option('-u', '--upstream', default='origin',
              help='Remote upstream URL.')
@click.option('--addons-dir', 'addons_dirs', multiple=True,
              type=click.Path(file_okay=False, exists=True),
              help="Directory containing addons. Defaults to odoo/addons or "
                   "odoo_addons if present. This option can be repeated.")
@click.option('-r', '--diff-requirements', 'diff_requirements', is_flag=True,
              help="Defines whether the comparison must take the requirements "
                   "file into account or not.")
@click.pass_context
def addons_toupdate(ctx, git_ref, tmp_dir, upstream, addons_dirs,
                    diff_requirements):
    repo_url = check_output(['git', 'remote', 'get-url', upstream])
    if not repo_url:
        raise click.ClickException(
            "No repository found for given upstream name."
            "{upstream_name}".format(upstream_name=upstream))
    if not addons_dirs:
        addons_dirs = get_default_addons_dirs()
    addon_names = []
    for addons_dir in addons_dirs:
        installable_addons = get_installable_addons([addons_dir])
        for addon_name in installable_addons:
            addon_dir = os.path.join(addons_dir, addon_name)
            if call(['git', 'diff', '--quiet', git_ref, addon_dir]):
                addon_names.append(addon_name)

    if diff_requirements:
        requirements_filename = 'requirements.txt'
        if not os.path.exists(requirements_filename):
            raise click.ClickException(
                "No requirements file found in the current project.")
        diff_requirements_filename = os.path.join(
            tmp_dir, requirements_filename)
        if not os.path.exists(diff_requirements_filename):
            click.echo('all')
            return
        with open(requirements_filename) as f:
            current_requirements = parse_requirements(f)
        with open(diff_requirements_filename) as f:
            diff_requirements = parse_requirements(f)
        for module_name in current_requirements:
            current_req = current_requirements.get(module_name)
            diff_req = diff_requirements.get(module_name)
            if not current_req or not diff_req:
                continue
            if module_name in ['odoo', 'odoo_addons_enterprise']:
                if current_req.specs != diff_req.specs or \
                        current_req.revision != diff_req.revision:
                    click.echo('all')
                    return
            if EXTERNAL_SOURCES_REGEX.match(module_name):
                if current_req.specs != diff_req.specs or \
                        current_req.revision != diff_req.revision:
                    click.echo('all')
                    return
            if ODOO_ADDON_REGEX.match(module_name):
                if current_req.editable != diff_req.editable:
                    addon_names.append(module_name)
                    continue
                if current_req.editable:
                    if current_req.revision != diff_req.revision:
                        addon_names.append(module_name)
                        continue
                    if current_req.uri != diff_req.uri:
                        addon_names.append(module_name)
                        continue
                else:
                    if current_req.specs != diff_req.specs:
                        addon_names.append(module_name)
                        continue

    click.echo(ctx.obj['separator'].join(addon_names))


addons.add_command(addons_toupdate, 'toupdate')
