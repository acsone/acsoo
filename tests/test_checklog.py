# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import unittest

from click.testing import CliRunner

from acsoo.checklog import checklog


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class TestChecklog(unittest.TestCase):

    def test1(self):
        runner = CliRunner()
        res = runner.invoke(checklog, [
            os.path.join(DATA_DIR, 'test1.log'),
        ])
        self.assertTrue(res.exit_code != 0)
        expected = "errors that caused failure (2):"
        self.assertTrue(expected in res.output)

    def test2(self):
        runner = CliRunner()
        res = runner.invoke(checklog, [
            '--ignore', ' ERROR ',
            os.path.join(DATA_DIR, 'test1.log'),
        ])
        self.assertTrue(res.exit_code != 0)
        expected = "errors that caused failure (1):"
        self.assertTrue(expected in res.output)
        expected = "errors that did not cause failure (1):"
        self.assertTrue(expected in res.output)
