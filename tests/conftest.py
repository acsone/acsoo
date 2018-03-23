# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from os.path import join as opj
import pytest
from subprocess import check_call


@pytest.fixture(scope='session')
def initdir(tmpdir_factory):
    tmpdir = tmpdir_factory.getbasetemp()
    tmpdir.chdir()
    acsoo_repo = "https://github.com/acsone/acsoo.git"
    check_call(['git', 'clone', acsoo_repo, '--quiet'],
               cwd=tmpdir.strpath)
    check_call(['git', 'checkout',
                'cfdb4d310cd04ce0ea8098586007f7d561a1c0aa', '--quiet'],
               cwd=opj(tmpdir.strpath, 'acsoo'))
    return opj(tmpdir.strpath, 'acsoo/tests/data/addons_toupdate')
