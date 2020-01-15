Changes
~~~~~~~

.. Future (?)
.. ----------
.. -

2.0.0 (2020-01-15)
------------------

- [IMP] project template: publish html coverage in gitlab-ci
- [IMP] project template: branch coverage in gitlab-ci
- [IMP] project template: pre-commit cache in gitlab-ci
- [DEL] deprecate acsoo pylint in favor of pre-commit and per project .pylintrc
- [IMP] Odoo 13 support
- [IMP] project template: rename requirements-dev.txt to requirements.txt.in,
  better reflecting that these are input requirements and not requirements
  for the development environment
- [IMP] project template: update copyright year
- [IMP] project template: remove module_auto_update, use click-odoo-update instead

1.9.0 (2019-02-28)
------------------

- [IMP] project template: use pre-commit (black, isort, flake8)
- [FIX] project template: fail on click-odoo-update error
- [FIX] project template: fix deploy log file
- [FIX] acsoo pylint: compatibility with pylint 2

1.8.3 (2019-01-22)
------------------
- [FIX] acsoo pylint: Adapt config to also work with pytlint-odoo 2.0.1
- [IMP] project template: use click-odoo-update

1.8.2 (2018-11-05)
------------------
- [IMP] project template: better way to declare python version
  in .gitlab-ci.yml
- Fix acsoo tag for Odoo 12

1.8.1 (2018-10-30)
------------------
- [IMP] ignore pylint C0303 (https://github.com/PyCQA/pylint/issues/289)

1.8.0 (2018-10-29)
------------------
- [IMP] acsoo wheel: add --no-deps, so we can build requirements.txt without
  fetching dependencies, and later install the project with --no-index and
  --find-links=release/ so as to detect missing dependencies (#38)
- [IMP] acsoo wheel: add --exclude-project option (to build requirements.txt
  without the current project), in preparation of #44
- [IMP] acsoo wheel: use a cache of editable git dependencies
- [IMP] acsoo wheel: use pip wheel -e . to build project instead of
  setup.py bdist_wheel, since the reason we were doing that has apparently
  been resolved in recent pip version (pip issue 3499 referred in a comment
  is apparently unrelated unfortunately, so I'm not sure why we were
  doing that exactly, probably https://github.com/pypa/pip/issues/3500)
- [IMP] flake8: ignore W503 and W504 by default (line break around logical
  operators)
- [IMP] project template: Odoo 12 support
- [IMP] project template: pin acsoo version
- [IMP] project template: acsoo wheel --no-deps, so, combined with
  pip install --no-index in the test stage, it verifies that all dependencies
  are included in requirements.txt

1.7.1 (2018-07-15)
------------------
- [IMP] project template: add makepot in .gitlab-ci.yml
- [IMP] pylint: whitelist lxml c library

1.7.0 (2018-06-04)
------------------
- [IMP] more python 3 and Odoo 11 support
- [IMP] project template: build stage in gitlab-ci
- [IMP] project template: new style deploy / upgrade
  (using checksum upgrades and click-odoo-upgrade script)
- [IMP] project template: enforce odoo-autodiscover>=2 and do not use it
  for Odoo >= 11
- [IMP] add --dry-run option to acsoo tag and tag_requirements
- [IMP] make the list of places where tag_requirements can push
  configurable
- [IMP] project template: on demand installation of acsoo and ssh-agent
- [IMP] project template: use click-odoo-initdb in gitlab-ci

1.6.0 (2018-02-16)
------------------
- [IMP] checklog: add --no-err-if-empty option
- [IMP] python 3 support
- [IMP] preliminary Odoo 11 support
- [IMP] project template: various improvements
- [IMP] refactoring of get_installable_addons() method for better reusability

1.5.0 (2017-09-19)
------------------
- [IMP] tag_requirements: fetch more aggressively; this solves the errors
  trying to write ref with non existent object
- [IMP] tag: always tag requirements when doing acsoo tag
- [IMP] tag: tag requirements before tagging project, so if something fails
  when tagging the requirements the project is not tagged and the release
  build is not triggered.
- [ADD] addons: add --separator option (and fix tests that were not testing much)
- [IMP] addons: consider current dir as addons dir candidate
- [IMP] pylint: look for module to test in current dir by default, using the
  same algorithm as ``addons list``
- [IMP] pylint: support python 3 style odoo/addons namespace (without __init__.py)

1.4.3 (2017-06-16)
------------------
- [IMP] checklog: consider ignore lines starting with # as comments
- [FIX] checklog: the previous release broke checklog color output

1.4.2 (2017-06-16)
------------------
- [IMP] checklog: fail if no log record found in input
- [IMP] checklog: echo with click to be less sensitive to unicode issues

1.4.1 (2017-06-14)
------------------
- [FIX] regression in acsoo release

1.4.0 (2017-06-13)
------------------
- [IMP] colored logging
- [IMP] major change to acsoo tag and tag_editable_requirements. These changes
  make it easier to work with a CI-driven release process that is triggered on
  new tags. The usual manual ``acsoo release`` process should be mostly unimpacted by
  these changes.

  - ``tag_editable_requirements`` is now ``tag_requirements``.
  - the tags structure has changed from ``{series}-{trigram}_{version}`` to
    ``{series}-{trigram}-{req_sha}-{egg}``, where ``{req_sha}`` is the sha of the
    last change to ``requirements.txt``.
  - ``tag_requirements`` includes the egg name in the tag so different commits
    in the same repo can be tagged (before, all addons in a given dependency repo had
    to be on the same commit).
  - when a tag for the given series, trigram and egg already exists on the
    dependency commit, ``tag_requirements`` does not attempt to create another
    tag (this avoids creating useless tags or forced tags) and
    this is sufficient because the sole purpose of these dependency tags is
    to avoid commits to be garbage collected.
  - ``acsoo tag`` now invokes ``tag_requirements``. In most cases however this
    will not place additional tags on dependencies, because the normal workflow
    is to invoke ``tag_requirements`` as soon as ``requirements.txt`` is updated.
  - ``tag_requirements`` automatically transforms http(s) urls into ssh urls
    for the purpose of pushing tags. This allows to maximize the use of http(s)
    urls in requirements so CI and scripts do not require ssh access
    to the public dependencies. This currently only works for the acsone organization
    on github but the mechanism is easy to extend, should the need arise.

1.3.0 (2017-06-04)
------------------
- [IMP] flake8: read additional ``flake8-options`` in acsoo configuration file.
- [IMP] template: series-dependent odoo command in ``.gitlab.ci.yml``.
- [IMP] template: createdb in ``.gitlab-ci.yml`` because Odoo 8 does not do it by
  itself.
- [ADD] addons list-depends: ``--exclude`` option

1.2.2 (2017-05-30)
------------------
- [FIX] regression in ``tag``, ``tag_editable_requirements`` and ``release`` commands.

1.2.1 (2017-05-27)
------------------
- [IMP] add possibility to provide main config file as option.
- [IMP] checklog: read default options from ``[checklog]`` section of config file.
- [IMP] pylint: read default options from ``[pylint]`` section of config file.
- [IMP] pylint: the module or package to lint may be provided with ``-m``.
- [IMP] flake8: read default options from ``[flake8]`` section of config file.
  The only option so far is ``config`` to provide an alternate flake8
  configuration file. This is useful so developer only need to type
  ``acsoo flake8`` locally, even when a specific configuration is needed,
  so it's trivial to run locally with the same config as in CI.

1.1.0 (2017-05-25)
------------------
- [IMP] pylint: BREAKING the package to test must be provided explicitly,
  as soon as additional pylint options are provided,
  so as to enable easy local testing of a subset of a project. Examples:
  ``acsoo pylint -- -d some-message odoo``, ``acsoo pylint -- odoo.addons.xyz``;
- [IMP] pylint: disable more code complexity errors: ``too-many-nested-blocks``,
  ``too-many-return-statements``.
- [IMP] pylint: display messages causing failure last, so emails from CI.
  that show the last lines of the log are more relevant.
- [IMP] pylint: display summary of messages that did not cause failure, also
  when there is no failure.
- [ADD] ``acsoo addons list`` and ``acsoo addons list-depends``.
- [ADD] ``acsoo checklog``.

1.0.1 (2017-05-21)
------------------
- First public release.
