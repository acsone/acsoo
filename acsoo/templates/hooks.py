import os
import shutil
from ..tools import check_output


def pre_render_project(configurator):
    variables = configurator.variables
    odoo_serie = variables['odoo.series']

    if odoo_serie in ('11.0',):
        python_version = 'python3'
    else:
        python_version = 'python'

    configurator.variables['python_version'] = python_version
    configurator.variables['python_path'] = check_output([
        'which', python_version,
    ])


def post_render_project(configurator):
    variables = configurator.variables
    root = configurator.target_directory
    root = os.path.join(root, variables['project.name'])
    odoo_serie = variables['odoo.series']
    if odoo_serie in ('8.0', '9.0'):
        shutil.rmtree(os.path.join(root, 'odoo'))
    else:
        shutil.rmtree(os.path.join(root, 'odoo_addons'))

    if odoo_serie in ('11.0'):
        # Delete init file
        filename = '__init__.py'
        os.remove(os.path.join(root, 'odoo', filename))
        os.remove(os.path.join(root, 'odoo', 'addons', filename))
