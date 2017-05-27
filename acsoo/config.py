# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
from ConfigParser import ConfigParser

import click


CONFIG_FILE = 'acsoo.cfg'
SECTION = 'acsoo'


class AcsooConfig(object):

    def __init__(self, filename):
        self.__cfg = ConfigParser()
        if os.path.isfile(filename):
            self.__cfg.read(filename)

    @property
    def series(self):
        r = self.__cfg.get(SECTION, 'series')
        if not r:
            raise click.ClickException('Missing series in {}.'.
                                       format(CONFIG_FILE))
        if r not in ('8.0', '9.0', '10.0'):
            raise click.ClickException('Unsupported series {} in {}.'.
                                       format(r, CONFIG_FILE))
        return r

    @property
    def version(self):
        r = self.__cfg.get(SECTION, 'version')
        if not r:
            raise click.ClickException('Missing version in {}.'.
                                       format(CONFIG_FILE))
        return r

    @property
    def trigram(self):
        r = self.__cfg.get(SECTION, 'trigram')
        if not r:
            raise click.ClickException('Missing trigram in {}.'.format(
                CONFIG_FILE))
        return r
