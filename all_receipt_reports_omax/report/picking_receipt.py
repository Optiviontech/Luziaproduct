# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

from odoo import api, fields, models ,SUPERUSER_ID
from odoo.exceptions import UserError

class PickingOperationReceiptReport(models.AbstractModel):
    _name = 'report.all_receipt_reports_omax.receipt_picking_operation'
    _description = 'Picking Operations Receipt Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.picking'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'stock.picking',
            'docs': docs,
            'proforma': True
        }
        
class DeliverySlipReceiptReport(models.AbstractModel):
    _name = 'report.all_receipt_reports_omax.receipt_delivery_slip'
    _description = 'Delivery Slip Receipt Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['stock.picking'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'stock.picking',
            'docs': docs,
            'proforma': True
        }
