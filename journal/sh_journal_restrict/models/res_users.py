# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.
"""Module for extending res.users model."""

from odoo import api, fields, models


class ShResUsers(models.Model):
    """Inherited to add journal fields to res.users model."""
    _inherit = 'res.users'

    @api.model
    def default_get(self, fields):
        """Override to set default journals for the user."""
        rec = super().default_get(fields)

        journals = self.env.company.journal_ids.ids
        rec.update({
            'journal_ids': [(6, 0, journals)]
        })
        return rec

    journal_ids = fields.Many2many(
        'account.journal', string="Journals", copy=False,help="Select the journals this user has access to.")
