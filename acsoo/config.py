# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from ConfigParser import ConfigParser


CONFIG_FILE = 'acsoo.cfg'
SECTION = 'acsoo'


class AcsooConfig(object):

    def __init__(self):
        self.__cfg = ConfigParser()
        self.__cfg.read(CONFIG_FILE)

    @property
    def series(self):
        r = self.__cfg.get(SECTION, 'series')
        if not r:
            raise RuntimeError('Missing series in {}'.format(CONFIG_FILE))
        if r not in ('8.0', '9.0'):
            raise RuntimeError('Unsupported series %s'.format(r))
        return r

    @property
    def version(self):
        r = self.__cfg.get(SECTION, 'version')
        if not r:
            raise RuntimeError('Missing version in {}'.format(CONFIG_FILE))
        return r

    @property
    def trigram(self):
        r = self.__cfg.get(SECTION, 'trigram')
        if not r:
            raise RuntimeError('Missing trigram in {}'.format(CONFIG_FILE))
        return r


_config = AcsooConfig()


def config():
    return _config
