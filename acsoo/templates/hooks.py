import os
import shutil

ODOO_PYTHON2 = ("8.0", "9.0", "10.0")
ODOO_KEEP_INIT_PY = ODOO_PYTHON2
ODOO_LEGACY_NS = ("8.0", "9.0")


def pre_render_project(configurator):
    variables = configurator.variables
    odoo_series = variables["odoo.series"]

    if odoo_series in ODOO_PYTHON2:
        python_version = "python"
    else:
        python_version = "python3"

    configurator.variables["python_version"] = python_version
    configurator.variables["odoo.major"] = int(odoo_series.split(".")[0])


def post_render_project(configurator):
    variables = configurator.variables
    root = configurator.target_directory
    root = os.path.join(root, variables["project.name"])
    odoo_series = variables["odoo.series"]
    if odoo_series in ODOO_LEGACY_NS:
        shutil.rmtree(os.path.join(root, "odoo"))
    else:
        shutil.rmtree(os.path.join(root, "odoo_addons"))

    if odoo_series not in ODOO_KEEP_INIT_PY:
        # Delete init file
        filename = "__init__.py"
        os.remove(os.path.join(root, "odoo", filename))
        os.remove(os.path.join(root, "odoo", "addons", filename))
