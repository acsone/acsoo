import os
import shutil


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
