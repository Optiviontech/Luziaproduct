# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details

from odoo import api, fields, models ,SUPERUSER_ID
from odoo.exceptions import UserError

class InvoiceReceiptReport(models.AbstractModel):
    _name = 'report.all_receipt_reports_omax.receipt_invoice'
    _description = 'Invoice Receipt Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'account.move',
            'docs': docs,
            'proforma': True
        }
        
class InvoiceWithoutPaymentReceiptReport(models.AbstractModel):
    _name = 'report.all_receipt_reports_omax.receipt_invoicewithoutpayment'
    _description = 'Invoice Without Payment Receipt Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.move'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'account.move',
            'docs': docs,
            'proforma': True
        }
        
class PaymentSlipReceiptReport(models.AbstractModel):
    _name = 'report.all_receipt_reports_omax.receipt_payment_slip'
    _description = 'Payment Slip Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        docs = self.env['account.payment'].browse(docids)
        return {
            'doc_ids': docs.ids,
            'doc_model': 'account.payment',
            'docs': docs,
            'proforma': True
        }
