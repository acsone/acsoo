#!/bin/bash
set -e

REQS=requirements.txt

cat requirements-find-links.txt > $REQS

pip freeze |
  grep -v -E 'odoo-addons-{{ name }}|acsoo|^pudb|^Pygments|^urwid|^pkg-resources|^click' >> $REQS
