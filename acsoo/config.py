# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from ConfigParser import ConfigParser

import click


CONFIG_FILE = 'acsoo.cfg'
SECTION = 'acsoo'


class AcsooConfig(object):

    def __init__(self, config_file=CONFIG_FILE):
        self.__cfg = ConfigParser()
        self.__cfg.read(config_file)
        self.config_file = config_file

    @property
    def series(self):
        r = self.__cfg.get(SECTION, 'series')
        if not r:
            raise click.ClickException('Missing series in {}.'.
                                       format(self.config_file))
        if r not in ('8.0', '9.0', '10.0'):
            raise click.ClickException('Unsupported series {} in {}.'.
                                       format(r, self.config_file))
        return r

    @property
    def version(self):
        r = self.__cfg.get(SECTION, 'version')
        if not r:
            raise click.ClickException('Missing version in {}.'.
                                       format(self.config_file))
        return r

    @property
    def trigram(self):
        r = self.__cfg.get(SECTION, 'trigram')
        if not r:
            raise click.ClickException('Missing trigram in {}.'.format(
                self.config_file))
        return r


_config = None


def config(config_file):
    global _config
    if _config is None:
        _config = AcsooConfig(config_file.name)
    return _config
