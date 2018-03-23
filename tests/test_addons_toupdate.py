# -*- coding: utf-8 -*-
# Copyright 2017 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from subprocess import check_call

from click.testing import CliRunner

from acsoo.main import main
from acsoo.tools import working_directory


def _checkout_to(tmpdir, git_ref):
    check_call(['git', 'checkout', git_ref, '--quiet'], cwd=tmpdir)


def test_addon_toupdate_00(initdir):
    """
    Data:
        - addon_1 exists
        - no requirements file
    Test case:
        - compare against the same revision
        - compare requirements: YES
    Expected result:
        - exit code != 0 (no requirements file)
    """
    runner = CliRunner()
    _checkout_to(initdir, 'cfdb4d310cd04ce0ea8098586007f7d561a1c0aa')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            'cfdb4d310cd04ce0ea8098586007f7d561a1c0aa',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 != res.exit_code


def test_addon_toupdate_01(initdir):
    """
    Data:
        - addon_1 exists
        - no requirements file
    Test case:
        - add a new requirements file with only a find-links in it
        - compare requirements: NO
    Expected result:
        - /
    """
    runner = CliRunner()
    _checkout_to(initdir, 'fd2f1b3f463a541c01bf611a939f6129166d72fd')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            'cfdb4d310cd04ce0ea8098586007f7d561a1c0aa',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = '\n'
        assert expected == res.output


def test_addon_toupdate_02(initdir):
    """
    Data:
        - addon_1 exists
        - no requirements file
    Test case:
        - add a new requirements file with only a find-links in it
        - compare requirements: YES
    Expected result:
        - all
    """
    runner = CliRunner()
    _checkout_to(initdir, 'fd2f1b3f463a541c01bf611a939f6129166d72fd')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            'cfdb4d310cd04ce0ea8098586007f7d561a1c0aa',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = 'all\n'
        assert expected == res.output


def test_addon_toupdate_03(initdir):
    """
    Data:
        - addon_1 exists
        - requirements file exists
    Test case:
        - add a new dependency in requirements file on external library
        - compare requirements: YES
    Expected result:
        - /
    """
    runner = CliRunner()
    _checkout_to(initdir, '95c9bcf5823ef8b5af6c8e23073331b3bbb3bd6b')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            'fd2f1b3f463a541c01bf611a939f6129166d72fd',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = '\n'
        assert expected == res.output


def test_addon_toupdate_04(initdir):
    """
    Data:
        - addon_1 exists
        - requirements file exists
    Test case:
        - add a new non-editable dependency in requirements file on
          odoo addon
        - compare requirements: YES
    Expected result:
        - /
    """
    runner = CliRunner()
    _checkout_to(initdir, '5ce68ab261be5c280318f4c1c21545c6196c8438')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            '95c9bcf5823ef8b5af6c8e23073331b3bbb3bd6b',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = '\n'
        assert expected == res.output


def test_addon_toupdate_05(initdir):
    """
    Data:
        - addon_1 exists
        - requirements file exists
    Test case:
        - add a new editable dependency in requirements file on odoo addon
        - compare requirements: YES
    Expected result:
        - /
    """
    runner = CliRunner()
    _checkout_to(initdir, '8959e3f5d1c6fea33c1cfe5f395b371c7c865832')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            '5ce68ab261be5c280318f4c1c21545c6196c8438',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = '\n'
        assert expected == res.output


def test_addon_toupdate_06(initdir):
    """
    Data:
        - addon_1 exists
        - requirements file exists
    Test case:
        - change SHA of editable dependency on odoo addon
        - compare requirements: YES
    Expected result:
        - the changed addon's name (base_user_role)
    """
    runner = CliRunner()
    _checkout_to(initdir, 'b2220ef8486d8036e28f006f73bd7f4e1c48205f')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            '8959e3f5d1c6fea33c1cfe5f395b371c7c865832',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = 'base_user_role\n'
        assert expected == res.output


def test_addon_toupdate_07(initdir):
    """
    Data:
        - addon_1 exists
        - requirements file exists
    Test case:
        - add Odoo Community sources
        - compare requirements: YES
    Expected result:
        - /
    """
    runner = CliRunner()
    _checkout_to(initdir, '80800842ce88aaadbe56d939efcdc580e659d52a')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            'b2220ef8486d8036e28f006f73bd7f4e1c48205f',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = '\n'
        assert expected == res.output


def test_addon_toupdate_08(initdir):
    """
    Data:
        - addon_1 exists
        - requirements file exists
    Test case:
        - add external odoo addons sources
        - compare requirements: YES
    Expected result:
        - /
    """
    runner = CliRunner()
    _checkout_to(initdir, '48c3f00cf00a1c274a6c886c472d829ea7034d31')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            '80800842ce88aaadbe56d939efcdc580e659d52a',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = '\n'
        assert expected == res.output


def test_addon_toupdate_09(initdir):
    """
    Data:
        - addon_1 exists
        - requirements file exists
    Test case:
        - change Odoo Community sources SHA
        - compare requirements: YES
    Expected result:
        - all
    """
    runner = CliRunner()
    _checkout_to(initdir, '23dc800841ebf062476e7f74b20232f488b83c24')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            '48c3f00cf00a1c274a6c886c472d829ea7034d31',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = 'all\n'
        assert expected == res.output


def test_addon_toupdate_10(initdir):
    """
    Data:
        - addon_1 exists
        - requirements file exists
    Test case:
        - editable odoo addon dependency becomes non-editable
        - compare requirements: YES
    Expected result:
        - the changed addon's name (base_user_role)
    """
    runner = CliRunner()
    _checkout_to(initdir, '7fa79c44350536d1e97f72933dc6f1d09ad06139')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            '23dc800841ebf062476e7f74b20232f488b83c24',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = 'base_user_role\n'
        assert expected == res.output


def test_addon_toupdate_11(initdir):
    """
    Data:
        - addon_1 exists
        - requirements file exists
    Test case:
        - change external odoo addons sources SHA
        - compare requirements: YES
    Expected result:
        - all
    """
    runner = CliRunner()
    _checkout_to(initdir, 'c6a8763f7081a32b1d1935e8d81e05e8ade96726')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            '7fa79c44350536d1e97f72933dc6f1d09ad06139',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = 'all\n'
        assert expected == res.output


def test_addon_toupdate_12(initdir):
    """
    Data:
        - addon_1 exists
        - requirements file exists
    Test case:
        - change version of non-editable odoo addon
        - compare requirements: YES
    Expected result:
        - modified odoo addon's name (base_suspend_security)
    """
    runner = CliRunner()
    _checkout_to(initdir, '65a88b0a7f1427b9508862dcf3e440e70912c0be')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            'c6a8763f7081a32b1d1935e8d81e05e8ade96726',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = 'base_suspend_security\n'
        assert expected == res.output


def test_addon_toupdate_13(initdir):
    """
    Data:
        - addon_1 exists
        - requirements file exists
    Test case:
        - changes in addon_1
        - add addon_2
        - compare requirements: YES
    Expected result:
        - modified addon's name (addon_1)
    """
    runner = CliRunner()
    _checkout_to(initdir, '6d2cf0b76d459c45878d643825c82e7d2fc6951b')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            '65a88b0a7f1427b9508862dcf3e440e70912c0be',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = 'addon_1\n'
        assert expected == res.output


def test_addon_toupdate_14(initdir):
    """
    Data:
        - addon_1 exists
        - addon_2 exists
        - requirements file exists
    Test case:
        - add addon_3
        - compare requirements: YES
    Expected result:
        - /
    """
    runner = CliRunner()
    _checkout_to(initdir, '15150ba2150bd4b796b80a82972625440c1b4820')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            '6d2cf0b76d459c45878d643825c82e7d2fc6951b',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = '\n'
        assert expected == res.output


def test_addon_toupdate_15(initdir):
    """
    Data:
        - addon_1 exists
        - addon_2 exists
        - addon_3 exists
        - requirements file exists
    Test case:
        - remove addon_3
        - compare requirements: YES
    Expected result:
        - /
    """
    runner = CliRunner()
    _checkout_to(initdir, 'a01139afa02021954c0c9ffd899c794bb923fef9')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            '15150ba2150bd4b796b80a82972625440c1b4820',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = '\n'
        assert expected == res.output


def test_addon_toupdate_16(initdir):
    """
    Data:
        - addon_1 exists
        - addon_2 exists
        - requirements file exists
    Test case:
        - changes in addon_2
        - compare requirements: YES
    Expected result:
        - changed addon's name (addon_2)
    """
    runner = CliRunner()
    _checkout_to(initdir, '1c0e49e58f6a9b36c14becbbdb039cbca36f5293')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            'a01139afa02021954c0c9ffd899c794bb923fef9',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = 'addon_2\n'
        assert expected == res.output


def test_addon_toupdate_17(initdir):
    """
    Data:
        - addon_1 exists
        - addon_2 exists
        - requirements file exists
    Test case:
        - remove external odoo addons source
        - compare requirements: YES
    Expected result:
        - /
    """
    runner = CliRunner()
    _checkout_to(initdir, '3382b4e8afb086b0aaa4946f9bf9265c7a41c768')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            '1c0e49e58f6a9b36c14becbbdb039cbca36f5293',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = '\n'
        assert expected == res.output


def test_addon_toupdate_18(initdir):
    """
    Data:
        - addon_1 exists
        - addon_2 exists
        - requirements file exists
    Test case:
        - remove odoo addon dependency
        - compare requirements: YES
    Expected result:
        - /
    """
    runner = CliRunner()
    _checkout_to(initdir, 'bfde22f2c292ecc2921e1b7fc09b31bdf79b1f82')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            '3382b4e8afb086b0aaa4946f9bf9265c7a41c768',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = '\n'
        assert expected == res.output


def test_addon_toupdate_19(initdir):
    """
    Data:
        - addon_1 exists
        - addon_2 exists
        - requirements file exists
    Test case:
        - remove library dependency
        - compare requirements: YES
    Expected result:
        - /
    """
    runner = CliRunner()
    _checkout_to(initdir, '657f0f91012b35772c28e1d3ad936caada3ed64c')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            'bfde22f2c292ecc2921e1b7fc09b31bdf79b1f82',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = '\n'
        assert expected == res.output


def test_addon_toupdate_20(initdir):
    """
    Data:
        - addon_1 exists
        - requirements file exists
    Test case:
        - change editable odoo addon dependency URL
        - compare requirements: YES
    Expected result:
        - modified odoo addon's name (base_user_role)
    """
    runner = CliRunner()
    _checkout_to(initdir, '77d64b380dda00824f525d65f22d0677eb63eead')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            '72d6e17f5ae7df754c3bdad6d4603a9c0bc382c0',
            '-r',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 == res.exit_code
        expected = 'base_user_role\n'
        assert expected == res.output


def test_addon_toupdate_21(initdir):
    """
    Data:
        - addon_1 exists
        - requirements file exists
    Test case:
        - compared ref is not an ancestor of current ref
        - compare requirements: NO
    Expected result:
        - exit code != 0
    """
    runner = CliRunner()
    _checkout_to(initdir, 'cfdb4d310cd04ce0ea8098586007f7d561a1c0aa')
    with working_directory(initdir):
        res = runner.invoke(main, [
            'addons',
            'toupdate',
            '5ce68ab261be5c280318f4c1c21545c6196c8438',
            '--requirement',
            './requirements.txt',
        ])
        assert 0 != res.exit_code
