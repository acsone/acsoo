# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import unittest

from click.testing import CliRunner

from acsoo.main import main
from acsoo.tools import working_directory


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class TestAddons(unittest.TestCase):

    def test_list(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(main, [
                'addons',
                'list',
            ])
            assert res.exit_code == 0
            expected = 'addon1'
            assert expected in res.output

    def test_exclude(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(main, [
                'addons',
                '--exclude', 'addon1',
                'list',
            ])
            assert res.exit_code == 0
            expected = ''
            assert expected in res.output

    def test_include(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(main, [
                'addons',
                '--include', 'addon1',
                'list',
            ])
            assert res.exit_code == 0
            expected = 'addon1'
            assert expected in res.output

    def test_list_depends(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(main, [
                'addons',
                'list-depends',
            ])
            assert res.exit_code == 0
            expected = 'base'
            assert expected in res.output

    def test_list_depends_exclude(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(main, [
                'addons',
                'list-depends',
                '--exclude=base',
            ])
            assert res.exit_code == 0
            expected = ''
            assert expected in res.output
