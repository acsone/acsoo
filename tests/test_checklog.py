# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import unittest

from click.testing import CliRunner

from acsoo.checklog import checklog
from acsoo.main import main

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


class TestChecklog(unittest.TestCase):
    def test1(self):
        runner = CliRunner()
        res = runner.invoke(checklog, [os.path.join(DATA_DIR, "test1.log")])
        assert res.exit_code != 0
        expected = "errors that caused failure (2):"
        assert expected in res.output

    def test2(self):
        runner = CliRunner()
        res = runner.invoke(
            checklog, ["--ignore", " ERROR ", os.path.join(DATA_DIR, "test1.log")]
        )
        assert res.exit_code != 0
        expected = "errors that caused failure (1):"
        assert expected in res.output
        expected = "errors that did not cause failure (1):"
        assert expected in res.output

    def test3(self):
        runner = CliRunner()
        res = runner.invoke(
            checklog,
            ["-i", " ERROR ", "-i", " CRITICAL ", os.path.join(DATA_DIR, "test1.log")],
        )
        assert res.exit_code == 0
        expected = "errors that did not cause failure (2):"
        assert expected in res.output

    def test4(self):
        runner = CliRunner()
        res = runner.invoke(
            main,
            [
                "-c",
                os.path.join(DATA_DIR, "test_checklog.cfg"),
                "checklog",
                os.path.join(DATA_DIR, "test1.log"),
            ],
        )
        assert res.exit_code != 0
        expected = "errors that caused failure (1):"
        assert expected in res.output
        expected = "errors that did not cause failure (1):"
        assert expected in res.output

    def test_empty(self):
        runner = CliRunner()
        res = runner.invoke(checklog, [os.path.join(DATA_DIR, "empty.log")])
        assert res.exit_code != 0
        expected = "No Odoo log record found in input."
        assert expected in res.output
        res = runner.invoke(
            checklog, ["--no-err-if-empty", os.path.join(DATA_DIR, "empty.log")]
        )
        assert res.exit_code == 0
