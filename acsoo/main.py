# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import logging
from pkg_resources import get_distribution, DistributionNotFound

import click

from .config import AcsooConfig

try:
    __version__ = get_distribution('acsoo').version
except DistributionNotFound:
    # package is not installed
    pass

__notice__ = '''%(prog)s, version %(version)s

Acsone Odoo Development Tools.

Copyright 2016-2017 ACSONE SA/NV (<http://acsone.eu>)
License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).'''


class ColoredFormatter(logging.Formatter):

    COLORS = {
        'DEBUG': dict(dim=True),
        'INFO': dict(),
        'WARNING': dict(fg='yellow'),
        'ERROR': dict(fg='red'),
        'CRITICAL': dict(fg='white', bg='red'),
    }

    def format(self, record):
        res = super(ColoredFormatter, self).format(record)
        return click.style(res, **self.COLORS[record.levelname])


@click.group()
@click.version_option(version=__version__, message=__notice__)
@click.option('-v', '--verbose', count=True)
@click.option('-c', '--config', type=click.Path(dir_okay=False, exists=True),
              help="Configuration file (default: ./acsoo.cfg).")
@click.pass_context
def main(ctx, verbose, config):
    config = AcsooConfig(config)

    ctx.obj = dict(config=config)

    ctx.default_map = config.get_default_map()

    if verbose > 1:
        level = logging.DEBUG
    elif verbose > 0:
        level = logging.INFO
    else:
        level = logging.WARNING

    logger = logging.getLogger()
    channel = logging.StreamHandler()
    channel.setFormatter(ColoredFormatter())
    logger.setLevel(level)
    logger.addHandler(channel)
