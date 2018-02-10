# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
from textwrap import dedent

from click.testing import CliRunner

from acsoo.main import main


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


def test_posix():
    runner = CliRunner()
    for cmd in ([], ['posix']):
        res = runner.invoke(main, [
            'pgenv',
            '-c', os.path.join(DATA_DIR, 'pgenv.cfg'),
        ] + cmd)
        assert res.exit_code == 0
        expected = dedent("""\
            PGUSER=""; export PGUSER
            PGDATABASE="thedb"; export PGDATABASE
        """)
        assert expected == res.output


def test_exec(capfd):
    runner = CliRunner()
    res = runner.invoke(main, [
        'pgenv',
        '-c', os.path.join(DATA_DIR, 'pgenv.cfg'),
        'exec', '--', 'sh', '-c', 'echo $PGDATABASE',
    ])
    assert res.exit_code == 0
    out, __ = capfd.readouterr()
    assert "thedb\n" == out
