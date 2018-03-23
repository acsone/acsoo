# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import re
import requirements

import click

from .addons import addons, _split_set
from .tools import call, check_output


# Identifies external Odoo addon dependency
ODOO_ADDON_REGEX = re.compile(
    r'(?P<prefix>odoo[0-9]+[-_]addon[-_])(?P<addon_name>.*)'
)
# Identifies another distribution providing several addons
ODOO_ADDONS_REGEX = re.compile(
    r'(?P<prefix>odoo[-_]addons[-_])(?P<addons_name>.*)'
)
ODOO_REGEX = re.compile(
    r'(^odoo$)|(^odoo.*enterprise$)'
)


def _odoo_addon_dependency_changed(req_name, current_req, diff_req):
    """
    This method defines whether the odoo addon dependency has changed.
    :param req_name: odoo addon requirement name
    :param current_req: current requirement line of the addon
    :param diff_req: requirements line of the addon in the git ref
    :return: False if the addon dependency hasn't changed or if it's not
    an Odoo addon dependency, True otherwise
    """
    # Compare external odoo addons dependencies
    odoo_addon_match = ODOO_ADDON_REGEX.match(req_name)
    if not odoo_addon_match:
        return False
    # Previously editable or newly editable
    if current_req.editable != diff_req.editable:
        return True
    if current_req.editable:  # Editable dependency
        if current_req.revision != diff_req.revision:  # New revision
            return True
        if current_req.uri != diff_req.uri:  # URL changed
            return True
    else:  # Not editable dependency
        if current_req.specs != diff_req.specs:  # New version
            return True
    return False


def _get_dependencies_toupdate(requirement, git_ref):
    """
    This method parses and compare the requirements file of the current
    version and the given one.
    :param requirement: requirements file name
    :return: list of changed dependencies or 'all'
    """
    dependencies = set()
    diff_req_ref = git_ref + ':' + requirement
    if not os.path.exists(requirement):
        raise click.ClickException(
            "Requirements file not found. No '{req_file}' file has been "
            "found in the project. Please create the file or do not "
            "enable the requirements comparison.".format(
                req_file=requirement))
    with open(requirement) as req_file:
        requirements_string = req_file.read()
    try:
        devnull = open(os.devnull, 'w')
        diff_requirements_string = check_output(
            ['git', 'show', diff_req_ref], stderr=devnull)
    except click.ClickException:  # The requirements file is new
        return 'all'
    # If requirements are the same, stop
    if requirements_string == diff_requirements_string:
        return dependencies
    # Parse the requirements files
    current_requirements = {
        req.name.replace('-', '_'):
            req for req in requirements.parse(requirements_string)}
    diff_requirements = {
        req.name.replace('-', '_'):
            req for req in requirements.parse(diff_requirements_string)}
    # Compare the two requirements files and populate modified addons list
    for req_name in current_requirements:
        current_req = current_requirements.get(req_name)
        diff_req = diff_requirements.get(req_name)
        if not diff_req:  # New dependency, ignore
            continue
        # Special case for odoo and enterprise addons, update all if change
        if ODOO_REGEX.match(req_name) and \
                (current_req.specs != diff_req.specs or
                 current_req.revision != diff_req.revision):
            return 'all'
        # Special case for external sources, update all if change
        # TODO: recursive comparison of the changes in the external sources
        if ODOO_ADDONS_REGEX.match(req_name) and \
                (current_req.specs != diff_req.specs or
                 current_req.revision != diff_req.revision):
            return 'all'
        if _odoo_addon_dependency_changed(req_name, current_req, diff_req):
            dependencies.add(
                ODOO_ADDON_REGEX.match(req_name).group('addon_name'))
    return dependencies


@click.command(help="Print a comma separated list of the modified installable "
                    "addons from the given git ref")
@click.argument('git_ref')
@click.option('-r', '--diff-requirements', 'diff_requirements', is_flag=True,
              help="Defines whether the comparison must take the requirements "
                   "file into account or not.")
@click.option('--exclude', default='',
              help="Comma separated list of addons to exclude from "
                   "the dependencies.")
@click.option('--requirement', default='requirements.txt',
              type=click.Path(dir_okay=False, exists=True),
              help='Requirements to use for requirements comparison '
                   '(default=requirements.txt)')
@click.pass_context
def addons_toupdate(ctx, git_ref, diff_requirements, exclude, requirement):
    # Check ancestor
    if call(['git', 'merge-base', '--is-ancestor', git_ref, 'HEAD']):
        click.echo('all')
        return
    addon_names = set()
    # Compare each installable addons and populate modified addons set
    addons = ctx.obj['addons']
    for addon_name, (addon_dir, manifest) in addons.items():
        if call(['git', 'diff', '--quiet', '--diff-filter=M',
                 git_ref, addon_dir]):
            addon_names.add(addon_name)
    if not diff_requirements:
        click.echo(ctx.obj['separator'].join(sorted(addon_names)))
        return
    # Requirements file comparison
    dependency_names = _get_dependencies_toupdate(requirement, git_ref)
    if dependency_names == 'all':
        click.echo('all')
        return
    # Remove excluded dependencies from addons list
    exclude = _split_set(exclude)
    dependency_names -= exclude
    addon_names |= dependency_names
    click.echo(ctx.obj['separator'].join(sorted(addon_names)))


addons.add_command(addons_toupdate, 'toupdate')
