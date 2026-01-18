# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

"""This file defines configuration settings for stock picking and scrap operations."""

from odoo import fields, models


class ResCompany(models.Model):
    """Extension of res.company to include operation type settings for stock and scrap."""

    _inherit = 'res.company'

    picking_operation_type = fields.Selection([
        ('cancel', 'Cancel Only'),
        ('cancel_draft', 'Cancel and Reset to Draft'),
        ('cancel_delete', 'Cancel and Delete')],
        default='cancel',
        string="Stock Picking Operation Type"
    )

    scrap_operation_type = fields.Selection([
        ('cancel', 'Cancel Only'),
        ('cancel_draft', 'Cancel and Reset to Draft'),
        ('cancel_delete', 'Cancel and Delete')],
        default='cancel',
        string="Scrap Operation Type"
    )


class ResConfigSettings(models.TransientModel):
    """Settings view for stock and scrap operation types."""

    _inherit = 'res.config.settings'

    picking_operation_type = fields.Selection(
        default=lambda self: self.env.company.picking_operation_type,
        string="Stock Picking Operation Type",
        related="company_id.picking_operation_type",
        readonly=False,
        help="Defines the operation type when cancelling a stock picking."
    )

    scrap_operation_type = fields.Selection(
        default=lambda self: self.env.company.scrap_operation_type,
        string="Scrap Operation Type",
        related="company_id.scrap_operation_type",
        readonly=False,
        help="Defines the operation type when cancelling a scrap order."
    )
