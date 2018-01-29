# -*- coding: utf-8 -*-
# Copyright 2016-2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import contextlib
import logging
import os
import subprocess
import sys
import tempfile
from contextlib import contextmanager
from distutils.spawn import find_executable as _fe

import click

_logger = logging.getLogger(__name__)


def _escape(s):
    s = s.replace('\\', '\\\\')
    s = s.replace('"', '\\"')
    s = s.replace('\'', '\\\'')
    s = s.replace('&', '\\&')
    s = s.replace('|', '\\|')
    s = s.replace('>', '\\>')
    s = s.replace('<', '\\<')
    s = s.replace(' ', '\\ ')
    return s


@contextmanager
def tempinput(data):
    temp = tempfile.NamedTemporaryFile(delete=False)
    temp.write(data)
    temp.close()
    try:
        yield temp.name
    finally:
        os.unlink(temp.name)


def cmd_commit(paths_to_commit, message, skip_ci=True):
    if paths_to_commit:
        add_cmd = ['git', 'add']
        add_cmd.extend(paths_to_commit)
        check_call(add_cmd)
        if skip_ci:
            message = "%s [ci skip]" % message
        check_call(['git', 'commit', '-m', message])
    else:
        click.echo('Nothing to commit')


def cmd_push(git_push_branch=None, git_remote_url=None):
    if not git_push_branch:
        git_push_branch = check_output(
            ['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        git_push_branch = git_push_branch.strip('\n')
    if git_remote_url:
        old_origin = check_output(['git', 'remote', 'get-url', 'origin'])
        old_origin = old_origin.replace('\n', '')
        check_call(['git', 'remote', 'set-url', 'origin', git_remote_url])
        click.echo('Change remote origin to %s ...' % git_remote_url)
    if not check_output(
            ['git', 'ls-remote', '--heads', 'origin', git_push_branch]):
        click.echo('%s not a branch : skipping ...' % git_push_branch)
    else:
        check_call(['git', 'pull', '--no-ff', 'origin', git_push_branch])
        check_call(['git', 'push', 'origin', 'HEAD:%s' % git_push_branch])
        if git_remote_url:
            check_call(['git', 'remote', 'set-url', 'origin', old_origin])
            click.echo('Restore remote origin ...')


def cmd_string(cmd):
    return " ".join([_escape(s) for s in cmd])


def log_cmd(cmd, cwd=None, level=logging.DEBUG, echo=False):
    s = cmd_string(cmd)
    if echo:
        click.echo(click.style(s, bold=True))
    _logger.log(level, '%s$ %s', cwd or '.', s)


def call(cmd, cwd=None, log_level=logging.DEBUG, echo=False):
    _adapt_executable(cmd)
    log_cmd(cmd, cwd=cwd, level=log_level, echo=echo)
    try:
        return subprocess.call(cmd, cwd=cwd)
    except subprocess.CalledProcessError:
        raise click.ClickException(cmd_string(cmd))


def check_call(cmd, cwd=None, log_level=logging.DEBUG, echo=False):
    _adapt_executable(cmd)
    log_cmd(cmd, cwd=cwd, level=log_level, echo=echo)
    try:
        return subprocess.check_call(cmd, cwd=cwd)
    except subprocess.CalledProcessError:
        raise click.ClickException(cmd_string(cmd))


def check_output(
        cmd, cwd=None, log_level=logging.DEBUG, echo=False,
        universal_newlines=True):
    _adapt_executable(cmd)
    log_cmd(cmd, cwd=cwd, level=log_level, echo=echo)
    try:
        return subprocess.check_output(
            cmd, cwd=cwd, universal_newlines=universal_newlines)
    except subprocess.CalledProcessError:
        raise click.ClickException(cmd_string(cmd))


@contextlib.contextmanager
def working_directory(path):
    """A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    """
    prev_cwd = os.getcwd()
    _logger.debug('.$ cd %s', _escape(path))
    os.chdir(path)
    try:
        yield
    finally:
        _logger.debug('.$ cd %s', _escape(prev_cwd))
        os.chdir(prev_cwd)


def _adapt_executable(cmd):
    cmd[0] = _find_executable(cmd[0])


def _find_executable(exe):
    python_dir = os.path.dirname(sys.executable)
    exe_path = os.path.join(python_dir, exe)
    if os.path.exists(exe_path):
        return exe_path
    exe_path = _fe(exe)
    if exe_path:
        return exe_path
    raise RuntimeError("%s executable not found" % (exe, ))


def cfg_path(filename):
    return os.path.join(os.path.dirname(__file__), 'cfg', filename)
