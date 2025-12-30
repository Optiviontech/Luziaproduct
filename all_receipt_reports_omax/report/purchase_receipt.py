# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

from odoo import api, fields, models ,SUPERUSER_ID
from odoo.exceptions import UserError

class PurchaseOrderReceiptReport(models.AbstractModel):
    _name = 'report.all_receipt_reports_omax.receipt_purchase_order'
    _description = 'Purchase Order Receipt Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['purchase.order'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'purchase.order',
            'docs': docs,
            'proforma': True
        }
        
class RFQReceiptReport(models.AbstractModel):
    _name = 'report.all_receipt_reports_omax.receipt_rfq'
    _description = 'Request For Quotation Receipt Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['purchase.order'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'purchase.order',
            'docs': docs,
            'proforma': True
        }

