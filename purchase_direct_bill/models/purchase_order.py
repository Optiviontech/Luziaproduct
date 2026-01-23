# -*- coding: utf-8 -*-
from odoo import api, models, _
from odoo.exceptions import UserError


class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    def action_create_bill_direct(self):
        """
        :return: Action to open the created bill
        """
        return self.action_create_invoice(attachment_ids=False)
