# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
from os.path import join as opj
import unittest

from click.testing import CliRunner

from acsoo.main import main
from acsoo.tools import working_directory


DATA_DIR = opj(os.path.dirname(__file__), 'data')


class TestAddons(unittest.TestCase):

    def test_list(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(main, [
                'addons',
                'list',
            ])
            assert res.exit_code == 0
            expected = 'addon1,addon2\n'
            assert expected == res.output

    def test_exclude(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(main, [
                'addons',
                '--exclude', 'addon1',
                'list',
            ])
            assert res.exit_code == 0
            expected = 'addon2\n'
            assert expected == res.output

    def test_include(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(main, [
                'addons',
                '--include', 'addon1',
                'list',
            ])
            assert res.exit_code == 0
            expected = 'addon1\n'
            assert expected == res.output

    def test_list_depends(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(main, [
                'addons',
                'list-depends',
            ])
            assert res.exit_code == 0
            expected = 'base\n'
            assert expected == res.output

    def test_list_depends_exclude(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(main, [
                'addons',
                'list-depends',
                '--exclude=base',
            ])
            assert res.exit_code == 0
            expected = '\n'
            assert expected == res.output

    def test_separator(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(main, [
                'addons',
                '--separator', ';',
                'list',
            ])
            assert res.exit_code == 0
            expected = 'addon1;addon2\n'
            assert expected == res.output

    def test_addons_in_cur_dir(self):
        runner = CliRunner()
        with working_directory(opj(DATA_DIR, 'odoo', 'addons')):
            res = runner.invoke(main, [
                'addons',
                '--separator', ';',
                'list',
            ])
            assert res.exit_code == 0
            expected = 'addon1;addon2\n'
            assert expected == res.output
