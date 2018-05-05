# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import click

from .main import main
from .manifest import get_installable_addons
from .addons_makepot import do_makepot
from .click_option import RequiredDepends
from .config import AcsooConfig


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


@click.command()
@click.option('--database')
@click.option('--odoo-bin', 'odoo_bin', default='odoo')
@click.option('--odoo-config', 'odoo_config',
              type=click.Path(dir_okay=False, exists=True))
@click.option('--git-commit', 'git_commit', is_flag=True, default=False)
@click.option(
    '--create-languages', default='',
    help="Comma separated list of languages for which the .po files will "
         "be created if not present.")
@click.option('--addons-regex')
@click.pass_context
def makepot(ctx, database, odoo_bin, odoo_config, git_commit,
            create_languages, addons_regex):
    addons = ctx.obj['addons']
    create_languages = _split_set(create_languages)
    do_makepot(database, odoo_bin, addons, odoo_config, git_commit,
               create_languages, addons_regex)


addons.add_command(makepot)


def _read_defaults(config):
    section = 'acsoo'
    defaults = dict(
        languages=config.get(
            section, 'languages', default='__new__'),
    )
    return dict(addons=defaults)


AcsooConfig.add_default_map_reader(_read_defaults)
