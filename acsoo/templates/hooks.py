import os
import shutil


def pre_render_project(configurator):
    variables = configurator.variables
    odoo_series = variables['odoo.series']

    if odoo_series in ('11.0', '12.0'):
        python_version = 'python3'
    else:
        python_version = 'python'

    configurator.variables['python_version'] = python_version
    configurator.variables['odoo.major'] = int(odoo_series.split('.')[0])


def post_render_project(configurator):
    variables = configurator.variables
    root = configurator.target_directory
    root = os.path.join(root, variables['project.name'])
    odoo_series = variables['odoo.series']
    if odoo_series in ('8.0', '9.0'):
        shutil.rmtree(os.path.join(root, 'odoo'))
    else:
        shutil.rmtree(os.path.join(root, 'odoo_addons'))

    if odoo_series in ('11.0'):
        # Delete init file
        filename = '__init__.py'
        os.remove(os.path.join(root, 'odoo', filename))
        os.remove(os.path.join(root, 'odoo', 'addons', filename))
