# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

from odoo import api, fields, models ,SUPERUSER_ID
from odoo.exceptions import UserError

class SalesReceiptReport(models.AbstractModel):

    _name = 'report.all_receipt_reports_omax.receipt_sale_order'
    _description = 'Sales Receipt Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['sale.order'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'sale.order',
            'docs': docs,
            'proforma': True
        }

