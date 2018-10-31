# -*- coding: utf-8 -*-
# Copyright © 2015 ACSONE SA/NV
# License LGPLv3 (http://www.gnu.org/licenses/lgpl-3.0-standalone.html)

import ast
import os

MANIFEST_NAMES = ("__openerp__.py", "__manifest__.py", "__terp__.py")


class NoManifestFound(Exception):
    pass


def get_manifest_path(addon_dir):
    for manifest_name in MANIFEST_NAMES:
        manifest_path = os.path.join(addon_dir, manifest_name)
        if os.path.isfile(manifest_path):
            return manifest_path


def parse_manifest(s):
    return ast.literal_eval(s)


def get_default_addons_dirs():
    addons_dirs = []
    candidate_addons_dirs = (os.path.join("odoo", "addons"), "odoo_addons", ".")
    for addons_dir in candidate_addons_dirs:
        if os.path.isdir(addons_dir):
            addons_dirs.append(addons_dir)
    return addons_dirs


def get_installable_addons(addons_dirs=None):
    """
    This method builds a dictionary of all installable addons in the specified
    addons directory or in the default addons directories.
    :param addons_dirs: path to the addons directories to fetch into
    :return: Dictionary like: {'addon_name': (addons_directory, manifest)}
    where manifest is a dictionary.
    """
    if not addons_dirs:
        addons_dirs = get_default_addons_dirs()
    res = {}
    for addons_dir in addons_dirs:
        for addon_name in os.listdir(addons_dir):
            addon_dir = os.path.join(addons_dir, addon_name)
            manifest_path = get_manifest_path(addon_dir)
            if not manifest_path:
                continue
            with open(manifest_path) as f:
                manifest = parse_manifest(f.read())
            if not manifest.get("installable", True):
                continue
            res[addon_name] = (addon_dir, manifest)
    return res
