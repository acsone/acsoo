# acsoo - Acsone Odoo Dev Tools

This is a set of command-line utilities to facilitate
the Odoo development workflow at Acsone.

It assumes the project is a setuptools-based python package
that can be packaged and installed with pip.

Criteria for tools to be included here:

* being sufficiently non-trivial to be error-prone or time consuming when done manually
* being used across several Acsone Odoo projects

## What we have here

Try acsoo --help.

### acsoo tag

Tag the current project after ensuring everything has 
been commited to git.

### acsoo tag_editable_requirements

Tag all editable requirements found in requirements.txt, so
the commits referenced in there are not lost in case of
git garbage collection.

### acsoo bdist_wheels

Build wheels for all dependencies found in requirements.txt,
plus the project in the current directory.

This is actually almost trivial, but works around a pip quirk.

### acsoo release

Perform acsoo tag, tag_editable_requirements and bdist_wheels.

## Ideas

### acsoo init-module (to replace https://github.com/acsone/odoo-scaffold-templates)

### acsoo init-project (if only to show the canonical project template) 
