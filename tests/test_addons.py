# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import unittest

from click.testing import CliRunner

from acsoo.addons import addons
from acsoo.tools import working_directory


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class TestPylint(unittest.TestCase):

    def test_list(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(addons, [
                'list',
            ])
            self.assertTrue(res.exit_code == 0)
            expected = 'addon1'
            assert expected in res.output

    def test_depends(self):
        runner = CliRunner()
        with working_directory(DATA_DIR):
            res = runner.invoke(addons, [
                'depends',
            ])
            self.assertTrue(res.exit_code == 0)
            expected = 'base'
            assert expected in res.output
