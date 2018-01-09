# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import re

import click

from .main import main
from .manifest import get_installable_addons
from .tools import call, check_output, parse_requirements


# Identifies external Odoo addon dependency
ODOO_ADDON_REGEX = re.compile(
    r'odoo[0-9]+[-_]addon[-_].*'
)
# Identifies another distribution providing several addons
ODOO_ADDONS_REGEX = re.compile(
    r'odoo[-_]addons[-_].*'
)
ODOO_REGEX = re.compile(
    r'(^odoo$)|(^odoo.*enterprise$)'
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
@click.option('-r', '--diff-requirements', 'diff_requirements', is_flag=True,
              help="Defines whether the comparison must take the requirements "
                   "file into account or not.")
@click.pass_context
def addons_toupdate(ctx, git_ref, diff_requirements):
    # Check ancestor
    if call(['git', 'merge-base', '--is-ancestor', 'HEAD', git_ref]):
        click.echo('all')
        return
    addon_names = []
    # Compare each installable addons and populate modified addons list
    addons_paths = ctx.obj['addons_paths']
    for addon_name in addons_paths:
        addon_dir = os.path.join(addons_paths[addon_name], addon_name)
        if call(['git', 'diff', '--quiet', git_ref, addon_dir]):
            addon_names.append(addon_name)
    # Requirements file comparison
    if diff_requirements:
        diff_req_ref = git_ref + ':' + 'requirements.txt'
        requirements_filename = "requirements.txt"
        if not os.path.exists(requirements_filename):
            raise click.ClickException(
                "No requirements file found in the current project.")
        with open(requirements_filename) as f:
            requirements_string = f.read()
        try:
            diff_requirements_string = check_output(
                ['git', 'show', diff_req_ref])
        except click.ClickException:
            click.echo('all')
            return
        # If requirements are the same, stop
        if requirements_string == diff_requirements_string:
            click.echo(ctx.obj['separator'].join(addon_names))
            return
        # Parse the requirements files
        current_requirements = parse_requirements(requirements_string)
        diff_requirements = parse_requirements(diff_requirements_string)
        # Compare the two requirements files and populate modified addons list
        for req_name in current_requirements:
            current_req = current_requirements.get(req_name)
            diff_req = diff_requirements.get(req_name)
            # New dependency, ignore
            if not diff_req:
                continue
            # Special case for odoo and enterprise addons, update all if change
            if ODOO_REGEX.match(req_name):
                if current_req.specs != diff_req.specs or \
                        current_req.revision != diff_req.revision:
                    click.echo('all')
                    return
            # Special case for external sources, update all if change
            # TODO: recursive comparison of the changes in the external sources
            if ODOO_ADDONS_REGEX.match(req_name):
                if current_req.specs != diff_req.specs or \
                        current_req.revision != diff_req.revision:
                    click.echo('all')
                    return
            # Compare external odoo addons dependencies
            if ODOO_ADDON_REGEX.match(req_name):
                # Previously editable or newly editable
                if current_req.editable != diff_req.editable:
                    addon_names.append(req_name)
                    continue
                if current_req.editable:
                    # New revision
                    if current_req.revision != diff_req.revision:
                        addon_names.append(req_name)
                        continue
                    # URL changed
                    if current_req.uri != diff_req.uri:
                        addon_names.append(req_name)
                        continue
                else:
                    # New version
                    if current_req.specs != diff_req.specs:
                        addon_names.append(req_name)
                        continue

    click.echo(ctx.obj['separator'].join(addon_names))


addons.add_command(addons_toupdate, 'toupdate')
