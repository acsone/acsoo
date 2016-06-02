# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from setuptools import setup, find_packages


setup(
    name='acsoo',
    description='Acsone Odoo Dev Tools',
    version='1.0.0a1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pip',  # TODO >= 8.2
        'setuptools>=20',
        'wheel>=0.29',
    ],
    entry_points='''
        [console_scripts]
        acsoo=acsoo.main:main
    ''',
)
