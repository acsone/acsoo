#!/bin/bash

# Pin build dependencies from requirements-build.txt.in.

set -e
VENV_DIR=$(mktemp -d)
trap "rm -rf $VENV_DIR" EXIT
python3 -m venv $VENV_DIR
source $VENV_DIR/bin/activate
if [ -f requirements-build.txt ] ; then
    CONSTRAINTS="-c requirements-build.txt"
else
    CONTRAINTS=""
fi
pip install -r requirements-build.txt.in $CONTRAINTS
pip freeze --all | grep -v "^pip==" > requirements-build.txt
