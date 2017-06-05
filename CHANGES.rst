Changes
~~~~~~~

.. Future (?)
.. ----------
.. -

Future (?)
----------
- [IMP] colored logging
- [IMP] tag_editable_requirements: include egg name in tag, so it is possible
  to have several requirements (ie Odoo addons) on different commits in the same repo.
- [IMP] tag, tag_editable_requirements: quiet git fetch and push

1.3.0 (2017-06-04)
------------------
- [IMP] flake8: read additional flake8-options in acsoo configuration file.
- [IMP] template: series-dependent odoo command in .gitlab.ci.yml.
- [IMP] template: createdb in .gitlab-ci.yml because in 8 Odoo does not do it by itself.
- [ADD] addons list-depends: --exclude option

1.2.2 (2017-05-30)
------------------
- [FIX] regression in tag, tag_editable_requirements and release commands.

1.2.1 (2017-05-27)
------------------
- [IMP] add possibility to provide main config file as option.
- [IMP] checklog: read default options from [checklog] section of config file.
- [IMP] pylint: read default options from [pylint] section of config file.
- [IMP] pylint: the module or package to lint may be provided with -m.
- [IMP] flake8: read default options from [flake8] section of config file.
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
