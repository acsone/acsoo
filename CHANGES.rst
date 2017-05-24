Changes
~~~~~~~

.. Future (?)
.. ----------
.. -

1.1.0 (2017-05-23)
------------------
- [IMP] pylint: disable more code complexity errors: too-many-nested-blocks, too-many-return-statements
- [IMP] pylint: BREAKING the package to test must be provided explicitly, so as to enable easy local testing
  of a subset of a project. Examples: acsoo pylint -- odoo, acsoo pylint -- odoo.addons.xyz
- [IMP] pylint: display messages causing failure last, so emails from CI that show the last lines of the log
  are more relevant

1.0.1 (2017-05-21)
------------------
- First public release.
