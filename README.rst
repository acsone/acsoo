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
* yet being sufficiently non-trivial to be error-prone or time consuming when done manually
* being used across several Acsone Odoo projects

Installation
~~~~~~~~~~~~

  .. code:: shell

    pip install acsoo

.. note::

   Since ``acsoo`` has a lot of dependencies that are not required at runtime, it
   is not recommanded to install it in the same virtualenv as your project.
   A good approach is to install it in it's own virtual env and symlink the ``acsoo``
   and ``mrbob`` executable somewhere in your PATH.

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

acsoo tag
---------

Tag the current project after ensuring everything has been commited to git.

acsoo tag_requirements
----------------------

Tag all VCS requirements found in ``requirements.txt``, so
the referenced commits are not lost in case of VCS garbage collection.

acsoo wheel
-----------

Build wheels for all dependencies found in ``requirements.txt``,
plus the project in the current directory.

This is actually almost trivial (ie ``pip wheel -r requirements.txt -e .``),
but works around a pip quirk.

acsoo release
-------------

Perform ``acsoo tag``, ``acsoo tag_requirements`` and
``acsoo wheel`` in one command.

acsoo flake8
------------

Run `flake8 <https://pypi.python.org/pypi/flake8>`_ with sensible default for Odoo code.

It is possible to pass additional options to the ``flake8`` command, eg:

  .. code:: shell

    acsoo flake8 -- --ignore E24,W504

acsoo pylint
------------

Run `pylint <https://pypi.python.org/pypi/pylint>`_ on the ``odoo`` or ``odoo_addons`` namespace.
It automatically uses the `pylint-odoo <https://pypi.python.org/pypi/pylint-odoo>`_ plugin and
runs with a reasonable configuration, including an opinionated set of disabled message.

It is possible to pass additional options to the ``pylint`` command, eg:

  .. code:: shell

    acsoo pylint -- --disable missing-final-newline odoo

This command returns an non-zero exit code if any message is reported.
It is however possibly to display messages while reporting success, eg:

  .. code:: shell

    acsoo pylint --expected api-one-deprecated:2,line-too-long -- odoo

The above command succeeds despite having exactly 2 ``api-one-deprecated`` or
any number of ``line-too-long`` messages being reported.

It is also possible to force failure on messages that are ``expected`` in the
default configuration, eg to fail on ``fixme`` errors, just expect 0 ``fixme`` messages, like this:

  .. code:: shell

    acsoo pylint --expected fixme:0 -- odoo

acsoo addons
------------

A set of commands to print addons lists, useful when running tests.

  .. code:: shell

     acsoo addons list
     acsoo addons list-depends

acsoo checklog
--------------

Check if an odoo log file contains error, with the possibility to ignore some
errors based on regular expressions.

  .. code:: shell

     acsoo checklog odoo.log
     odoo -d mydb -i base --stop-after-init | acsoo checklog
     acsoo checklog --ignore "WARNING.*blah" odoo.log

bumpversion
-----------
Bumpversion is a software automatically installed with acsoo. It allows you to increment or simply change the version of the project in several files at once, including acsoo.cfg.

  .. code:: shell

    bumpversion {part}

Where part is 'major', 'minor' or 'patch' (see `semantic versioning <http://semver.org/>`_).

Configure bumpversion by editing the .bumpversion.cfg config file at the root of your project.
See the bumpversion `documentation <https://pypi.python.org/pypi/bumpversion>`_ to go further (automatic commit, tag, customisation...).

Ideas
~~~~~

acsoo freeze
------------

``pip freeze`` (which works very well as is) with the following additions

* exluding some common dev tools that are not required in production
  (pudb, ipdb, acsoo, git-aggregator, setuptools-odoo...)
  and their dependencies unless such dependencies are required by the project
  (directly or indirectly).
* excluding the project itself (as usual for python requirements.txt files)

Inspiration to be found in https://pypi.python.org/pypi/pipdeptree, although I don't
think acsoo should depend on that, as it's only a thin wrapper around the ``pip`` api.

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
