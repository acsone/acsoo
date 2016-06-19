# acsoo - Acsone Odoo Dev Tools

This is a set of command-line utilities to facilitate
the Odoo development workflow at Acsone.

It assumes the project is a setuptools-based python package
that can be packaged and installed with pip.

Criteria for tools to be included here:

* being small wrappers around standard commands (`git`, `pip`, etc)
* yet being sufficiently non-trivial to be error-prone or time consuming when done manually
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

### Initialize a new project

```
mkdir project-dir
cd project-dir
mkvirtualenv project-dir -a .
pip install git+https://github.com/acsone/acsoo.git
mrbob acsoo:templates/project
```

## Ideas

### acsoo freeze

`pip freeze` (which works very well as is) with the following additions

* exluding some common dev tools that are not required in production 
(pudb, ipdb, acsoo, git-aggregator, setuptools-odoo...)
and their dependencies unless such dependencies are required by the project 
(directly or indirectly).
* excluding the project itself (as usual for python requirements.txt files)

Inspiration to be found in https://pypi.python.org/pypi/pipdeptree, although I don't
think acsoo should depend on that, as it's only a thin wrapper around the `pip` api.

### acsoo version

A helper to bump version in `acsoo.cfg` and also bump version in (some?) odoo addons, such
as the main addon that pulls dependencies. Requires further thinking.
