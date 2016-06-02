# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import contextlib
import logging
import os
import subprocess


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


def _log_cmd(cmd, cwd=None):
    cmd_string = " ".join([_escape(s) for s in cmd])
    _logger.debug('%s$ %s', cwd or '.', cmd_string)


def call(cmd, cwd=None):
    _log_cmd(cmd, cwd=cwd)
    return subprocess.call(cmd, cwd=cwd)


def check_call(cmd, cwd=None):
    _log_cmd(cmd, cwd=cwd)
    return subprocess.check_call(cmd, cwd=cwd)


def check_output(cmd, cwd=None):
    _log_cmd(cmd, cwd=cwd)
    return subprocess.check_output(cmd, cwd=cwd)


@contextlib.contextmanager
def working_directory(path):
    """A context manager which changes the working directory to the given
    path, and then changes it back to its previous value on exit.
    """
    _logger.debug('.$ cd %s', _escape(path))
    prev_cwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(prev_cwd)
