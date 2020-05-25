# -*- coding: utf-8 -*-
# Copyright 2016 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from setuptools import setup

setup(
    # this is still required for python setup.py sdist
    setup_requires=["setuptools_scm!=4.0.0"],
    use_scm_version=True,
)
