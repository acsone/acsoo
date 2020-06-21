import textwrap

import respx
from click.testing import CliRunner

from acsoo.pr_status import pr_status


@respx.mock
def test_pr_status_basic():
    req1 = respx.get(
        "https://api.github.com/repos/OCA/mis-builder/pulls/298",
        content='{"state": "closed", "merged": false}',
    )
    req2 = respx.get(
        "https://api.github.com/repos/OCA/server-tools/pulls/100",
        content='{"state": "closed", "merged": true}',
    )
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("requirements.txt.in", "w") as f:
            f.write(
                textwrap.dedent(
                    """\
                    # closed not merged
                    -e git+https//github.com/OCA/mis-builder@refs/pull/298/head#\
                    subdirectory=setup/mis_builder&egg=odoo13-addon-mis_builder
                    # closed and merged
                    odoo10-addon-suspend_security @ \
                    git+https//github.com/OCA/server-tools@refs/pull/100/head#\
                    subdirectory=setup/suspend_security
                    """
                )
            )
        res = runner.invoke(pr_status, color=False)
        assert req1.called
        assert req2.called
        assert res.exit_code == 0
        assert "OCA/mis-builder/pull/298 is closed" in res.output
        assert "OCA/server-tools/pull/100 is merged" in res.output
