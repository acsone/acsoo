#!/bin/bash
pip install -U "pip>=9.0.1"

# https://github.com/odoo/odoo/pull/15718
# https://github.com/pypa/pip/issues/4176
pip install -U "setuptools<31"
