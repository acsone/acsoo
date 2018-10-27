# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

from acsoo.cache import Cache


def tests_cache(tmp_path):

    cachedir = tmp_path / "cache"
    cachedir.mkdir()

    indir = tmp_path / "in"
    indir.mkdir()
    f1 = indir / "f1"
    f1.write_text(u"1" * int(1000000))
    f2 = indir / "f2"
    f2.write_text(u"2" * int(1000000))

    outdir = tmp_path / "out"
    outdir.mkdir()

    cache = Cache(str(cachedir))

    cache.put("key1", str(f1))

    fname = cache.get("key1", str(outdir))
    assert fname == "f1"
    assert ["f1"] == [x.name for x in outdir.iterdir()]

    fname = cache.get("key2", str(outdir))
    assert not fname
    assert ["f1"] == [x.name for x in outdir.iterdir()]

    cache.put("key2", str(f2))
    fname = cache.get("key2", str(outdir))
    assert fname == "f2"
    assert ["f1", "f2"] == sorted([x.name for x in outdir.iterdir()])

    cache.remove("key1")
    assert not cache.get("key1", str(outdir))
