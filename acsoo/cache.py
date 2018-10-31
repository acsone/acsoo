# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import errno
import hashlib
import os
import shutil

import appdirs


class Cache:
    def __init__(self, cachename):
        self.cachedir = os.path.join(appdirs.user_cache_dir(), cachename)
        if not os.path.exists(self.cachedir):
            os.makedirs(self.cachedir)
            with open(os.path.join(self.cachedir, "CACHEDIR.TAG"), "w") as f:
                f.write(
                    "Signature: 8a477f597d28d172789f06886806bc55\n"
                    "# This file is a cache directory tag created by 'acsoo'.\n"
                    "# For information about cache directory tags, see:\n"
                    "#	http://www.brynosaurus.com/cachedir/\n"
                )

    def _cachepath(self, key):
        hashed = hashlib.sha224(key.encode()).hexdigest()
        parts = [self.cachedir] + [hashed[:2], hashed[2:4], hashed[4:6], hashed[6:]]
        return os.path.join(*parts)

    def put(self, key, filepath):
        cachepath = self._cachepath(key)
        try:
            os.makedirs(cachepath)
        except OSError as e:
            if e.errno == errno.EEXIST:
                # already exists, someone else already put
                return
        try:
            shutil.copy(filepath, cachepath)
        except BaseException:
            shutil.rmtree(cachepath)
            raise

    def get(self, key, dirpath):
        assert os.path.isdir(dirpath)
        cachepath = self._cachepath(key)
        if not os.path.isdir(cachepath):
            # not in cache
            return
        filenames = os.listdir(cachepath)
        if len(filenames) != 1:
            # corrupted cache
            shutil.rmtree(cachepath)
            return
        filename = filenames[0]
        shutil.copy(os.path.join(cachepath, filename), dirpath)
        return filename

    def remove(self, key):
        cachepath = self._cachepath(key)
        shutil.rmtree(cachepath)
