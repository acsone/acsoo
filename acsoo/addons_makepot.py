# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import subprocess
import click
import time
from .tools import cmd_commit, cmd_push, tempinput
from .checklog import do_checklog

NEW_LANGUAGE = '__new__'


def do_makepot(database, odoo_bin, installable_addons, odoo_config, git_commit,
               git_push, languages, git_push_branch, git_remote_url):
    if not languages:
        languages = [NEW_LANGUAGE]
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
        stderr=subprocess.STDOUT)

    script_dir = os.path.dirname(__file__)
    installlang_script_path = os.path.join(script_dir, 'installlang_script')
    with open(installlang_script_path) as f:
        install_language_cmd = f.read()
    for lang in languages:
        if lang == NEW_LANGUAGE:
            continue
        lang_kwargs = {
            'lang': lang,
        }
        install_lang_cmd = install_language_cmd % lang_kwargs
        proc.stdin.write(install_lang_cmd)

    script_path = os.path.join(script_dir, 'makepot_script')
    with open(script_path) as f:
        script_cmd = f.read()
    files_to_commit = []
    for addon_name, (addon_dir, manifest) in installable_addons.items():
        if os.path.islink(addon_dir):
            click.echo("Module %s ignored : symlink" % addon_name)
            continue
        i18n_path = os.path.join(addon_dir, 'i18n')
        for lang in languages:
            if lang == NEW_LANGUAGE:
                file_name = '%s.pot' % addon_name
            else:
                file_name = '%s.po' % lang
            pot_file_path = os.path.join(i18n_path, file_name)
            kwargs = {
                'module_name': addon_name,
                'pot_file_path': pot_file_path,
                'lang': lang,
                'i18n_path': i18n_path,
            }
            module_cmd = script_cmd % kwargs
            proc.stdin.write(module_cmd)
            files_to_commit.append(pot_file_path)
    proc.stdin.close()
    out = proc.stdout.read()
    proc.wait()
    file_to_remove = set([])
    for file in files_to_commit:
        if not os.path.exists(file):
            file_to_remove.add(file)
    files_to_commit = set(files_to_commit) - file_to_remove
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
    if git_commit or git_push:
        cmd_commit(files_to_commit, "Update translation files")

    if git_push:
        cmd_push(git_push_branch=git_push_branch,
                 git_remote_url=git_remote_url)
