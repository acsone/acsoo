Changes
~~~~~~~

.. Future (?)
.. ----------
.. -

1.4.2 (2017-06-16)
------------------
- [IMP] acsoo checklog: fail if no log record found in input
- [IMP] acsoo checklog: echo with click to be less sensitive to unicode issues

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
- [IMP] template: createdb in ``.gitlab-ci.yml`` because Odoo 8 does not do it by itself.
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
