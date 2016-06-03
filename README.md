# acsoo - Acsone Odoo Dev Tools

This is a set of command-line utilities to facilitate
the Odoo development workflow at Acsone.

It assumes the project is a setuptools-based python package
that can be packaged and installed with pip.

Criteria for tools to be included here:

* being sufficiently non-trivial to be error-prone or time consuming when done manually
* being used across several Acsone Odoo projects

## What we have here

Try `acsoo --help`.

### acsoo tag

Tag the current project after ensuring everything has been commited to git.

### acsoo tag_editable_requirements

Tag all editable requirements found in `requirements.txt`, so
the referenced commits are not lost in case of git garbage collection.

### acsoo wheel

Build wheels for all dependencies found in `requirements.txt`,
plus the project in the current directory.

This is actually almost trivial (ie `pip wheel -r requirements.txt`),
but works around a pip quirk.

### acsoo release

Perform `acsoo tag`, `acsoo tag_editable_requirements` and
`acsoo wheel` in one command.

## Ideas

### acsoo init-module

To replace https://github.com/acsone/odoo-scaffold-templates

### acsoo init-project

If only to show the canonical project template.

### acsoo freeze

`pip freeze` (which works very well as is), but exluding some common dev tools
that are not required in production (pudb, ipdb, acsoo, git-aggregator, setuptools-odoo...)
and their dependencies unless such dependencies are required by the project (directly or indirectly).

### acsoo version

A helper to bump version in `acsoo.cfg` and also bump version in (some?) odoo addons, such
as the main addon that pulls dependencies. Requires further thinking.
