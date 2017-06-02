# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from setuptools import setup, find_packages


setup(
    name='acsoo',
    description='Acsone Odoo Dev Tools',
    long_description='\n'.join((
        open('README.rst').read(),
        open('CHANGES.rst').read(),
    )),
    use_scm_version=True,
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'bobtemplates.odoo',
        'click',
        'flake8',
        'lxml',  # pylint-odoo dep not installed automatically?
        'pip>=9.0.1',
        'pylint-odoo',
        'setuptools>=20,<31',
        'wheel>=0.29',
        'bumpversion',
    ],
    license='GPLv3+',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: '
        'GNU General Public License v3 or later (GPLv3+)',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 2.7',
        'Framework :: Odoo',
    ],
    setup_requires=[
        'setuptools-git',
        'setuptools-scm',
    ],
    entry_points='''
        [console_scripts]
        acsoo=acsoo.main:main
    ''',
)
