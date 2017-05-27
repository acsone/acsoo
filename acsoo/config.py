# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
from ConfigParser import RawConfigParser, NoOptionError, NoSectionError

import click


DEFAULT_CONFIG_FILE = 'acsoo.cfg'
SECTION = 'acsoo'


def _split_multiline(s):
    return [i.strip() for i in s.splitlines() if i.strip()]


class AcsooConfig(object):

    # list of callables returning dictionaries to update default_map
    default_map_readers = []

    def __init__(self, filename):
        self.__cfg = RawConfigParser()
        if not filename and os.path.isfile(DEFAULT_CONFIG_FILE):
            filename = DEFAULT_CONFIG_FILE
        if filename:
            if not os.path.isfile(filename):
                raise click.ClickException("Configuration file {} not found.".
                                           format(filename))
            self.__cfgfile = filename
            self.__cfg.read(filename)

    @staticmethod
    def add_default_map_reader(reader):
        AcsooConfig.default_map_readers.append(reader)

    def get_default_map(self):
        default_map = {}
        for reader in self.default_map_readers:
            default_map.update(reader(self))
        return default_map

    @property
    def series(self):
        r = self.__cfg.get(SECTION, 'series')
        if not r:
            raise click.ClickException('Missing series in {}.'.
                                       format(self.__cfgfile))
        if r not in ('8.0', '9.0', '10.0'):
            raise click.ClickException('Unsupported series {} in {}.'.
                                       format(r, self.__cfgfile))
        return r

    @property
    def version(self):
        r = self.__cfg.get(SECTION, 'version')
        if not r:
            raise click.ClickException('Missing version in {}.'.
                                       format(self.__cfgfile))
        return r

    @property
    def trigram(self):
        r = self.__cfg.get(SECTION, 'trigram')
        if not r:
            raise click.ClickException('Missing trigram in {}.'.
                                       format(self.__cfgfile))
        return r

    def get(self, section, option, default=None, flatten=False):
        try:
            r = self.__cfg.get(section, option)
            if flatten:
                r = ''.join(_split_multiline(r))
            return r
        except (NoOptionError, NoSectionError):
            return default

    def getboolean(self, section, option, default=None):
        try:
            return self.__cfg.getboolean(section, option)
        except (NoOptionError, NoSectionError):
            return default

    def getlist(self, section, option, default=None):
        try:
            return _split_multiline(self.__cfg.get(section, option))
        except (NoOptionError, NoSectionError):
            return default or []
