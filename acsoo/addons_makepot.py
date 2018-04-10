# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import subprocess
import click
import re
from .tools import cmd_commit, cmd_push, tempinput
from .checklog import do_checklog

NEW_LANGUAGE = '__new__'


def do_makepot(database, odoo_bin, installable_addons, odoo_config, git_commit,
               git_push, languages, git_push_branch, git_remote_url,
               addons_regex):
    odoo_shell_cmd = [
        odoo_bin,
        'shell',
        '-d', database,
        '--log-level=error',
        '--no-xmlrpc',
    ]
    if odoo_config:
        odoo_shell_cmd.extend([
            '-c', odoo_config
        ])
    proc = subprocess.Popen(
        odoo_shell_cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT, universal_newlines=True)

    script_dir = os.path.dirname(__file__)
    script_path = os.path.join(script_dir, 'makepot_script')
    with open(script_path) as f:
        script_cmd = f.read()
    files_to_commit = []
    addons_regex = addons_regex and re.compile(addons_regex) or False
    for addon_name, (addon_dir, manifest) in installable_addons.items():
        if addons_regex and not addons_regex.match(addon_name):
            click.echo("Module %s ignored : not matching" % addon_name)
            continue
        if os.path.islink(addon_dir):
            click.echo("Module %s ignored : symlink" % addon_name)
            continue
        i18n_path = os.path.join(addon_dir, 'i18n')
        file_name = '%s.pot' % addon_name
        pot_file_path = os.path.join(i18n_path, file_name)
        kwargs = {
            'module_name': addon_name,
            'pot_file_path': pot_file_path,
            'languages': languages,
            'i18n_path': i18n_path,
        }
        module_cmd = script_cmd % kwargs
        proc.stdin.write(module_cmd)
        files_to_commit.append(pot_file_path)
        for lang in languages:
            lang_file_path = os.path.join(i18n_path, '%s.po' % lang)
            files_to_commit.append(lang_file_path)
    proc.stdin.close()
    out = proc.stdout.read()
    proc.wait()
    click.echo(out)
    if out:
        with tempinput(out) as tempfilename:
            try:
                do_checklog(tempfilename, [], None)
            except click.ClickException as e:
                if e.message == "No Odoo log record found in input.":
                    pass
                else:
                    raise e
    file_to_remove = set([])
    for file in files_to_commit:
        if not os.path.exists(file):
            file_to_remove.add(file)
            continue
        out = subprocess.check_output([
            'git', 'diff', '--shortstat', file
        ], universal_newlines=True).strip()
        if not out:
            file_to_remove.add(file)
            continue
    files_to_commit = set(files_to_commit) - file_to_remove
    if git_commit or git_push:
        cmd_commit(files_to_commit, "Update translation files")

        if git_push:
            cmd_push(git_push_branch=git_push_branch,
                     git_remote_url=git_remote_url)
