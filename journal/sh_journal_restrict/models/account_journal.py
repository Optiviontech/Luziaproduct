# -*- coding: utf-8 -*-
# Part of Softhealer Technologies.

from odoo import api, fields, models
from odoo.osv import expression


class ShAccountJournalRestrict(models.Model):
    """Model for restricting journal access."""
    _inherit = 'account.journal'

    @api.model
    def default_get(self, field_list):
        """Override to set default users for the journal."""  
        rec = super().default_get(field_list)
        users = self.env.company.sh_user_ids.ids
        rec.update({
            'user_ids': [(6, 0, users)]
        })
        return rec

    user_ids = fields.Many2many(
        'res.users', string="Users", copy=False)

    
