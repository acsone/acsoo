# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import unittest
from textwrap import dedent

from click.testing import CliRunner

from acsoo.main import main
from acsoo.pylintcmd import pylintcmd
from acsoo.tools import working_directory


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class TestPylint(unittest.TestCase):

    def test1(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(pylintcmd, [
                '-e', 'fixme:0,manifest-required-key',
                '-m', 'odoo',
            ])
            self.assertTrue(res.exit_code != 0)
            expected = dedent("""\
                messages that did not cause failure:
                  manifest-required-key: 1
                messages that caused failure:
                  fixme: 1 (expected 0)
            """)
            assert expected in res.output

    def test2(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(pylintcmd, [
                '-e', 'fixme:0,manifest-required-key',
            ])
            self.assertTrue(res.exit_code != 0)
            expected = dedent("""\
                messages that did not cause failure:
                  manifest-required-key: 1
                messages that caused failure:
                  fixme: 1 (expected 0)
            """)
            assert expected in res.output

    def test2_config(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(main, [
                '-c', os.path.join(DATA_DIR, 'test_pylint2.cfg'),
                'pylint',
            ])
            self.assertTrue(res.exit_code != 0)
            expected = dedent("""\
                messages that did not cause failure:
                  manifest-required-key: 1
                messages that caused failure:
                  fixme: 1 (expected 0)
            """)
            assert expected in res.output

    def test3(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(pylintcmd, [
                '--', '-d', 'fixme',
            ])
            self.assertTrue(res.exit_code != 0)
            assert 'fixme: ' not in res.output

    def test3_config(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(main, [
                '-c', os.path.join(DATA_DIR, 'test_pylint3.cfg'),
                'pylint',
            ])
            self.assertTrue(res.exit_code != 0)
            assert 'fixme: ' not in res.output
