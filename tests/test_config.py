# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import unittest

from acsoo.config import AcsooConfig


DATA_DIR = os.path.join(os.path.dirname(__file__), 'data')


class TestConfig(unittest.TestCase):

    def setUp(self):
        self.config = AcsooConfig(os.path.join(DATA_DIR, 'test1.cfg'))

    def test1(self):
        assert self.config.get('test', 'absent') is None
        assert self.config.get('test', 'absent', 'default') == 'default'
        assert self.config.get('test', 'bool') == 'yes'
        assert self.config.get('test', 'multi') == '\nABC\nDEF'
        assert self.config.get('test', 'multi', flatten=True) == 'ABCDEF'
        assert self.config.getboolean('test', 'bool') is True
        assert self.config.getboolean('test', 'absent') is None
        assert self.config.getboolean('test', 'absent', False) is False
        assert self.config.getlist('test', 'multi') == ['ABC', 'DEF']
        assert self.config.getlist('test', 'absent') == []
        assert self.config.getlist('test', 'absent', ['A', 'B']) == ['A', 'B']
        assert self.config.get('absent', 'absent') is None
        assert self.config.getboolean('absent', 'absent') is None
        assert self.config.getlist('absent', 'absent') == []

    def test2(self):
        assert self.config.trigram == 'xyz'
        assert self.config.version == '1.1.0'
        assert self.config.series == '10.0'

    def test_default_map(self):
        default_map = self.config.get_default_map()
        assert default_map['checklog'] == {
            'ignore': ['WARNING', 'ERROR:.*registry'],
            'echo': None,
        }
