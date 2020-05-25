# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import os
import shutil

import appdirs
from click.testing import CliRunner

from acsoo.wheel import wheel


def test_wheel(mocker, tmp_path):
    # mock appdirs.user_cache_dir, so the cache
    # goes to a known place
    cachedir = tmp_path / "cache"
    mocker.patch.object(appdirs, "user_cache_dir", lambda: str(cachedir))
    runner = CliRunner()
    with runner.isolated_filesystem():
        with open("requirements.txt", "w") as f:
            f.write(
                "requests\n"
                "-e git+https://github.com/acsone/acsoo"
                "@178a896c360ed6059bb76da35af4e99815a8b8de"
                "#egg=acsoo\n"
            )
        res = runner.invoke(wheel, ["--no-deps", "--exclude-project"])
        assert res.exit_code == 0
        # acsoo wheel must be in cache
        cache_content = list(cachedir.glob("**/acsoo*.whl"))
        assert len(cache_content) == 1
        # two wheels must have been generated
        files = sorted(os.listdir("release"))
        assert len(files) == 2
        assert files[0].startswith("acsoo-2.0.2")
        assert files[1].startswith("requests")

        # run it again
        shutil.rmtree("release")
        res = runner.invoke(wheel, ["--no-deps", "--exclude-project"])
        assert res.exit_code == 0
        assert "Obtained -e git+https://github.com/acsone/acsoo" in res.output
        files = sorted(os.listdir("release"))
        assert len(files) == 2
        assert files[0].startswith("acsoo-2.0.2")
        assert files[1].startswith("requests")
