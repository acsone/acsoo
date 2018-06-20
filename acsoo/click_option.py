# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV (<http://acsone.eu>)
# License GPL-3.0 or later (http://www.gnu.org/licenses/gpl.html).

import click


class RequiredDepends(click.Option):
    """
    This class allows to tells that some options are required if the current
    one is used.
    """

    def __init__(self, *args, **kwargs):
        self.required_depends = kwargs.pop('required_depends', [])
        if not self.required_depends:
            raise click.BadArgumentUsage(
                "You have to declare the 'required_depends' argument "
                "containing a list of required option name."
            )
        self.required_depends_names = [
            self.get_original_option_name(name)
            for name in self.required_depends
        ]
        kwargs['help'] = kwargs.get('help', '') + \
            " NOTE: This argument requires following arguments: " + \
            ','.join(self.required_depends_names)
        super(RequiredDepends, self).__init__(*args, **kwargs)

    def handle_parse_result(self, ctx, opts, args):
        current_exists = self.name in opts
        depends_exists = all([
            option in opts
            for option in self.required_depends
        ])
        if current_exists and not depends_exists:
            raise click.UsageError(
                "'%s' requires following options: %s" % (
                    self.get_original_option_name(self.name),
                    ','.join(self.required_depends_names)
                ))
        return super(RequiredDepends, self).handle_parse_result(
            ctx, opts, args)

    @staticmethod
    def get_original_option_name(opt):
        return '--%s' % opt.replace('_', '-')
