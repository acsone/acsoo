import textwrap

from click.testing import CliRunner

from acsoo.pr_status import pr_status


def test_pr_status_basic():
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("requirements.txt.in", "w") as f:
            f.write(
                textwrap.dedent(
                    """\
                    # closed not merged
                    -e git+https://github.com/OCA/mis-builder@refs/pull/298/head#\
                    subdirectory=setup/mis_builder&egg=odoo13-addon-mis_builder
                    # closed and merged
                    odoo10-addon-suspend_security @ \
                    git+https://github.com/OCA/server-tools@refs/pull/100/head#\
                    subdirectory=setup/suspend_security
                    # closed and merged
                    odoo14-addon-mis_builder @ \
                    git+https://github.com/acsone/mis-builder@14.0-350-port#\
                    subdirectory=setup/mis_builder \
                    # https://github.com/OCA/mis-builder/pull/359
                    """
                )
            )
        res = runner.invoke(pr_status, color=False)
        assert res.exit_code == 0
        assert "OCA/mis-builder/pull/298 is closed" in res.output
        assert "OCA/server-tools/pull/100 is merged" in res.output
        assert "OCA/mis-builder/pull/359 is merged" in res.output
