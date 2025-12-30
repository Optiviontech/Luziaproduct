# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
"""Configuration for journal restriction settings."""

from odoo import fields, models


class ResCompany(models.Model):
    """Inherited to add journal and user fields to company settings."""
    _inherit = 'res.company'

    journal_ids = fields.Many2many('account.journal', string="Journals")
    sh_user_ids = fields.Many2many('res.users', string="Users", help="Users associated with this company.")


class ResConfigSettings(models.TransientModel):
    """Configuration for journal restriction settings."""
    _inherit = 'res.config.settings'

    journal_ids = fields.Many2many(
        related='company_id.journal_ids', readonly=False,
        help="Select the journals that will be restricted.")
    sh_user_ids = fields.Many2many(
        related='company_id.sh_user_ids', readonly=False,
        help="Select the users who will have restricted access to journals.")
