# -*- coding: utf-8 -*-
# Copyright (C) Softhealer Technologies.

from odoo import models, _

class Picking(models.Model):
    """Stock picking cancellation and unreserve logic."""

    _inherit = 'stock.picking'

    def _check_stock_account_installed(self):
        """Check if stock_account module is installed."""
        stock_account_app = self.env['ir.module.module'].sudo().search(
            [('name', '=', 'stock_account')], limit=1)
        return stock_account_app.state == 'installed'

    def action_picking_cancel(self):
        """Cancel the picking and related moves."""
        for rec in self:
            if rec.sudo().mapped('move_ids'):
                rec._sh_unreseve_qty()
                rec.sudo().mapped('move_ids').sudo().write({'state': 'cancel'})
                rec.sudo().mapped('move_ids').mapped('move_line_ids').sudo().write({'state': 'cancel'})

                if rec._check_stock_account_installed():
                    account_move = rec.sudo().mapped('move_ids').sudo().mapped('account_move_id')
                    account_move_line_ids = account_move.sudo().mapped('line_ids')
                    reconcile_ids = []
                    if account_move_line_ids:
                        reconcile_ids = account_move_line_ids.sudo().mapped('id')
                    reconcile_lines = self.env['account.partial.reconcile'].sudo().search(
                        ['|', ('credit_move_id', 'in', reconcile_ids), ('debit_move_id', 'in', reconcile_ids)])
                    if reconcile_lines:
                        reconcile_lines.sudo().unlink()
                    account_move.mapped('line_ids.analytic_line_ids').sudo().unlink()
                    account_move.sudo().write({'state': 'draft', 'name': '/'})
                    account_move.sudo().with_context(**{'force_delete': True}).unlink()

                    for move in rec.sudo().mapped('move_ids'):
                        if move.product_id:
                            product = move.product_id
                            cost_price = product.standard_price
                            qty = move.product_uom_qty
                            total_valuation = cost_price * qty

                        move.sudo().write({'state': 'cancel'})
            rec.sudo().write({'state': 'cancel'})

    def action_picking_cancel_draft(self):
        """Cancel the picking and set it to draft state."""
        for rec in self:
            if rec.sudo().mapped('move_ids'):
                rec._sh_unreseve_qty()
                rec.sudo().mapped('move_ids').sudo().write({'state': 'draft'})
                rec.sudo().mapped('move_ids').mapped('move_line_ids').sudo().write({'state': 'draft'})

                if rec._check_stock_account_installed():
                    account_move = rec.sudo().mapped('move_ids').sudo().mapped('account_move_id')
                    account_move_line_ids = account_move.sudo().mapped('line_ids')
                    reconcile_ids = []
                    if account_move_line_ids:
                        reconcile_ids = account_move_line_ids.sudo().mapped('id')
                    reconcile_lines = self.env['account.partial.reconcile'].sudo().search(
                        ['|', ('credit_move_id', 'in', reconcile_ids), ('debit_move_id', 'in', reconcile_ids)])
                    if reconcile_lines:
                        reconcile_lines.sudo().unlink()
                    account_move.mapped('line_ids.analytic_line_ids').sudo().unlink()
                    account_move.sudo().write({'state': 'draft', 'name': '/'})
                    account_move.sudo().with_context(**{'force_delete': True}).unlink()

                    for move in rec.sudo().mapped('move_ids'):
                        if move.product_id:
                            product = move.product_id
                            cost_price = product.standard_price
                            qty = move.product_uom_qty
                            total_valuation = cost_price * qty

                        move.sudo().write({'state': 'draft'})
            rec.sudo().write({'state': 'draft'})

    def action_picking_cancel_delete(self):
        """Cancel the picking and delete it."""
        for rec in self:
            if rec.sudo().mapped('move_ids'):
                rec._sh_unreseve_qty()
                rec.sudo().mapped('move_ids').sudo().write({'state': 'draft'})
                rec.sudo().mapped('move_ids').mapped('move_line_ids').sudo().write({'state': 'draft'})

                if rec._check_stock_account_installed():
                    account_move = rec.sudo().mapped('move_ids').sudo().mapped('account_move_id')
                    account_move_line_ids = account_move.sudo().mapped('line_ids')
                    reconcile_ids = []
                    if account_move_line_ids:
                        reconcile_ids = account_move_line_ids.sudo().mapped('id')
                    reconcile_lines = self.env['account.partial.reconcile'].sudo().search(
                        ['|', ('credit_move_id', 'in', reconcile_ids), ('debit_move_id', 'in', reconcile_ids)])
                    if reconcile_lines:
                        reconcile_lines.sudo().unlink()
                    account_move.mapped('line_ids.analytic_line_ids').sudo().unlink()
                    account_move.sudo().write({'state': 'draft', 'name': '/'})
                    account_move.sudo().with_context(**{'force_delete': True}).unlink()

                    for move in rec.sudo().mapped('move_ids'):
                        if move.product_id:
                            product = move.product_id
                            cost_price = product.standard_price
                            qty = move.product_uom_qty
                            total_valuation = cost_price * qty


                rec.sudo().mapped('move_ids').mapped('move_line_ids').sudo().unlink()
                rec.sudo().mapped('move_ids').sudo().unlink()
            rec.sudo().write({'state': 'draft'})
            rec.sudo().unlink()

    def _sh_unreseve_qty(self):
        """Unreserve the quantity of the product."""
        for move_line in self.sudo().mapped('move_ids').mapped('move_line_ids'):
            if move_line.product_id.type != 'consu':
                continue
            if self.state not in ['draft', 'cancel', 'assigned', 'waiting']:
                quant = self.env['stock.quant'].sudo().search([
                    ('location_id', '=', move_line.location_id.id),
                    ('product_id', '=', move_line.product_id.id),
                    ('lot_id', '=', move_line.lot_id.id),
                    ('package_id', '=', move_line.package_id.id),
                    ('product_id.is_storable', '=', True)], limit=1)
                if quant:
                    quant.write({'quantity': quant.quantity + move_line.quantity})
                elif move_line.product_id.is_storable:
                    self.env['stock.quant'].sudo().create({
                        'location_id': move_line.location_id.id,
                        'product_id': move_line.product_id.id,
                        'lot_id': move_line.lot_id.id,
                        'quantity': move_line.quantity,
                    })
                quant = self.env['stock.quant'].sudo().search([
                    ('location_id', '=', move_line.location_dest_id.id),
                    ('product_id', '=', move_line.product_id.id),
                    ('lot_id', '=', move_line.lot_id.id),
                    ('package_id', '=', move_line.result_package_id.id),
                    ('product_id.is_storable', '=', True)], limit=1)
                if quant:
                    quant.write({'quantity': quant.quantity - move_line.quantity})
                elif move_line.product_id.is_storable:
                    self.env['stock.quant'].sudo().create({
                        'location_id': move_line.location_dest_id.id,
                        'product_id': move_line.product_id.id,
                        'lot_id': move_line.lot_id.id,
                        'quantity': move_line.quantity * (-1),
                    })

    def sh_cancel(self):
        """Performs cancellation based on configured operation type."""
        if self.company_id.picking_operation_type == 'cancel':
            self.action_picking_cancel()
        elif self.company_id.picking_operation_type == 'cancel_draft':
            self.action_picking_cancel_draft()
        elif self.company_id.picking_operation_type == 'cancel_delete':
            self.action_picking_cancel_delete()
            return {
                'name': 'Inventory Transfer',
                'type': 'ir.actions.act_window',
                'res_model': 'stock.picking',
                'view_type': 'list',
                'view_mode': 'list,kanban,form',
                'target': 'current',
            }
