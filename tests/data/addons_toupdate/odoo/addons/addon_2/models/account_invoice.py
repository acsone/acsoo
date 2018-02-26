# -*- coding: utf-8 -*-
# Copyright 2018 ACSONE SA/NV
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    state = fields.Selection(
        string="State",
    )

    @api.multi
    def invoice_print(self):
        return super(AccountInvoice, self).invoice_print()
