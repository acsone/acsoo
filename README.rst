acsoo - Acsone Odoo Dev Tools
=============================

.. image:: https://img.shields.io/badge/license-GPL--3-blue.svg
   :target: http://www.gnu.org/licenses/gpl-3.0-standalone.html
   :alt: License: GPL-3
.. image:: https://badge.fury.io/py/acsoo.svg
    :target: http://badge.fury.io/py/acsoo
.. image:: https://travis-ci.org/acsone/acsoo.svg?branch=master
   :target: https://travis-ci.org/acsone/acsoo
.. image:: https://codecov.io/gh/acsone/acsoo/branch/master/graph/badge.svg
  :target: https://codecov.io/gh/acsone/acsoo

This is a set of command-line utilities to facilitate
the Odoo development workflow at Acsone.

It assumes the project is a setuptools-based python package
that can be packaged and installed with pip.

.. contents::

Criteria for tools to be included here:

* being small wrappers around standard commands (``git``, ``pip``, etc)
* yet being sufficiently non-trivial to be error-prone or time consuming when
  done manually
* being used across several Acsone Odoo projects

Installation
~~~~~~~~~~~~

.. code:: shell

   pip install --user acsoo

or

.. code:: shell

   pipx install acsoo

.. note::

   Since ``acsoo`` has a lot of dependencies that are not required at runtime,
   for your application, it is not recommanded to install it in the same
   virtualenv as your project.

To enable bash completion, add this line in your ``.bashrc``:

  .. code:: shell

     eval "$(_ACSOO_COMPLETE=source acsoo)"

What we have here
~~~~~~~~~~~~~~~~~

Below, the list of available commands with a few examples.

Use ``acsoo --help`` or ``acsoo <command> --help`` for more information.

Initialize a new project
------------------------

  .. code:: shell

    mrbob acsoo:templates/project
    cd {project name}
    mkvirtualenv {project name} -a .

acsoo pr-status
---------------

Look for git references of the form ``refs/pull/NNN/head`` in requirement
files and print the corresponding GitHub pull request status.

acsoo tag
---------

Tag the current project after ensuring everything has been commited to git.

acsoo tag-requirements
----------------------

Tag all VCS requirements found in ``requirements.txt``, so
the referenced commits are not lost in case of VCS garbage collection.

acsoo checklog
--------------

Check if an odoo log file contains error, with the possibility to ignore some
errors based on regular expressions.

  .. code:: shell

     acsoo checklog odoo.log
     odoo -d mydb -i base --stop-after-init | acsoo checklog
     acsoo checklog --ignore "WARNING.*blah" odoo.log

Deprecated commands
~~~~~~~~~~~~~~~~~~~

acsoo addons
------------

**acsoo addons is deprecated: use `manifestoo
<https://pypi.org/project/manifestoo>`_ instead: it is more robust and has
better test coverage.**

A set of commands to print addons lists, useful when running tests.

  .. code:: shell

     acsoo addons list
     acsoo addons list-depends

acsoo freeze
------------

**Deprecated: use `pip-deepfreeze <https://pypi.org/project/pip-deepfreeze>`_
instead.**

Just like pip freeze, except it outputs only dependencies of the provided
distribution name.

acsoo wheel
-----------

**This command is deprecated, use pip >= 20.1 and do not use editable VCS
dependencies. `pip wheel -e . -r requirements.txt --wheel-dir=release` will
then give the same result, including caching of pinned VCS dependencies.**

Build wheels for all dependencies found in ``requirements.txt``,
plus the project in the current directory.

The main advantage of this command (compared to a regular
`pip wheel -r requirements.txt -e . --wheel_dir=release --src src`),
was that it maintains a cache of git dependencies that are pinned with
a sha1.

acsoo release
-------------

**This command is deprecated. Releasing is automated via .gitlab-ci. See
the `build` stage in the project template.**

Perform ``acsoo tag``, ``acsoo tag_requirements`` and
``acsoo wheel`` in one command.

acsoo flake8
------------

**This command is deprecated, use a .flake8 file in your project,
in combination with pre-commit. See the project template for a reasonable default.**

Run `flake8 <https://pypi.python.org/pypi/flake8>`_ with sensible default for Odoo code.

It is possible to pass additional options to the ``flake8`` command, eg:

  .. code:: shell

    acsoo flake8 -- --ignore E24,W504

acsoo pylint
------------

**This command is deprecated, use a .pylintrc file in your project,
in combination with pre-commit. See the project template for a reasonable default.**

Run `pylint <https://pypi.python.org/pypi/pylint>`_ on detected Odoo addons in odoo/addons,
odoo_addons or the current directory.
It automatically uses the `pylint-odoo <https://pypi.python.org/pypi/pylint-odoo>`_ plugin and
runs with a reasonable configuration, including an opinionated set of disabled message.

It is possible to pass additional options to the ``pylint`` command, eg:

  .. code:: shell

    acsoo pylint -- --disable missing-final-newline

This command returns an non-zero exit code if any message is reported.
It is however possibly to display messages while reporting success, eg:

  .. code:: shell

    acsoo pylint --expected api-one-deprecated:2,line-too-long

The above command succeeds despite having exactly 2 ``api-one-deprecated`` or
any number of ``line-too-long`` messages being reported.

It is also possible to force failure on messages that are ``expected`` in the
default configuration, eg to fail on ``fixme`` errors, just expect 0 ``fixme``
messages, like this:

  .. code:: shell

    acsoo pylint --expected fixme:0

acsoo.cfg
~~~~~~~~~

A file named ``acsoo.cfg`` at the project root helps you set sensible defaults.

Here is a minimal example:

  .. code:: ini

    [acsoo]
    trigram=xyz
    series=10.0
    version=1.5.0

And a more elaborate example:

  .. code:: ini

    [acsoo]
    trigram=xyz
    series=11.0
    version=1.5.2
    pushable=
      github.com:acsone
      github.com:mozaik

    [checklog]
    ignore=
      WARNING .* module .*: description is empty !
      WARNING: unable to set column .* of table account_analytic_account not null

Useful links
~~~~~~~~~~~~

- pypi page: https://pypi.python.org/pypi/acsone
- code repository: https://github.com/acsone/acsoo
- report issues at: https://github.com/acsone/acsoo/issues

Maintainer
~~~~~~~~~~

.. image:: https://www.acsone.eu/logo.png
   :alt: ACSONE SA/NV
   :target: https://www.acsone.eu

This project is maintained by ACSONE SA/NV.
