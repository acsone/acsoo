def pre_render_project(configurator):
    variables = configurator.variables
    odoo_series = variables["odoo.series"]

    configurator.variables["odoo.major"] = int(odoo_series.split(".")[0])


def post_render_project(configurator):
    ...
