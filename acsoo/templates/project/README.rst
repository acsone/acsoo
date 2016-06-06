===============
Odoo {{ Name }}
===============

dev env howto
=============

1. Initialize virtualenv

create and activate virtualenv, possibly with virtualenvwrapper's
mkvirtualenv odoo-{{ name }} -a .

run ./bootstrap.sh

To save some time copy odoo {{ series }} sources in src/odoo

2. Install everything

pip install --src src -r requirements-dev.txt

3. run

odoo-autodiscover.py

4. freeze and release

update VERSION.txt
./freeze.sh
check what has changed in requirements.txt
commit everything
run acsoo release

# install it there as explained here:
# https://pip.pypa.io/en/stable/user_guide/#installation-bundles
