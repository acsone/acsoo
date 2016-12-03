import os
import shutil


def post_render_project(configurator):
    variables = configurator.variables
    root = configurator.target_directory
    root = os.path.join(root, variables['project.name'])
    if variables['odoo.series'] in ('8.0', '9.0'):
        shutil.rmtree(os.path.join(root, 'odoo'))
    else:
        shutil.rmtree(os.path.join(root, 'odoo_addons'))
