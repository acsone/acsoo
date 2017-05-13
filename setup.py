# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import re
from setuptools import setup, find_packages


def read(*parts):
    path = os.path.join(os.path.dirname(__file__), *parts)
    with open(path) as fobj:
        return fobj.read()


def find_version(*file_paths):
    version_file = read(*file_paths)
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]",
                              version_file, re.M)
    if version_match:
        return version_match.group(1)
    raise RuntimeError("Unable to find version string.")


setup(
    name='acsoo',
    description='Acsone Odoo Dev Tools',
    version=find_version('acsoo', 'main.py'),
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pip>=9.0.1',
        'setuptools>=20,<31',
        'wheel>=0.29',
        'bobtemplates.odoo',
        'flake8',
    ],
    setup_requires=[
        'setuptools-git',
    ],
    entry_points='''
        [console_scripts]
        acsoo=acsoo.main:main
    ''',
)
