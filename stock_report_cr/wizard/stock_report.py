# -*- coding: utf-8 -*-
# Part of Odoo Module Developed by CandidRoot Solutions Pvt. Ltd.
# See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api, _
import io
import base64
import logging
import pytz
import xlsxwriter

_logger = logging.getLogger(__name__)


class ReportWizard(models.TransientModel):
    _name = "stock.reports"
    _description = "Stock Report"

    start_date = fields.Datetime('Start Date', required=True)
    end_date = fields.Datetime('End Date', required=True)
    location_id = fields.Many2one('stock.location', 'Location', required=True)
    company_id = fields.Many2one(
        'res.company',
        string='Company',
        required=True,
        default=lambda self: self.env.company,
        domain="[('usage', '=', 'internal')]"
    )
    filterby = fields.Selection([
        ('no_filtred', 'No Filtered'),
        ('product', 'Product')],
        'Filter by',
        default='no_filtred'
    )
    products = fields.Many2many('product.product', 'products')
    group_by_category = fields.Boolean('Group By Category')

    xls_file = fields.Binary(string="XLS file")
    xls_filename = fields.Char()

    # -------------------------------------------------------------------------
    # Helper: Convert UTC datetime to user timezone
    # -------------------------------------------------------------------------
    def _convert_to_user_timezone(self, dt):
        if not dt:
            return False
        user_tz = pytz.timezone(self.env.user.tz or 'UTC')
        dt_utc = pytz.utc.localize(dt)
        local_dt = dt_utc.astimezone(user_tz)
        return local_dt.strftime('%Y-%m-%d %I:%M:%S %p')

    # -------------------------------------------------------------------------
    # PDF Export
    # -------------------------------------------------------------------------
    def button_export_pdf(self):
        start_date_utc = self.start_date
        end_date_utc = self.end_date
        StockMoveLine = self.env['stock.move.line']

        # Domain
        if not self.products:
            domain = [('date', '>=', start_date_utc), ('date', '<=', end_date_utc)]
            if self.location_id:
                domain.append(('location_dest_id', 'in', self.location_id.ids))
        else:
            domain = [
                ('date', '>=', start_date_utc), ('date', '<=', end_date_utc),
                ('product_id', 'in', self.products.ids)
            ]
            if self.location_id:
                domain.append(('location_dest_id', 'in', self.location_id.ids))

        # ✅ Using _read_group properly
        version_count_per_product = dict(
            StockMoveLine._read_group(
                domain=domain,
                groupby=['product_id'],
                aggregates=['id:count'],
            )
        )

        product_ids = [p.id for p in version_count_per_product.keys()]
        if not product_ids:
            return

        all_search = StockMoveLine.search([('product_id', 'in', product_ids)])

        search, product_list = [], []
        for each_item in all_search:
            if each_item.product_id.id not in product_list:
                search.append(each_item)
            product_list.append(each_item.product_id.id)

        move_lines = StockMoveLine.search([])
        incoming_dict, outgoing_dict = {}, {}
        for rec in move_lines:
            if rec.location_dest_id == self.location_id:
                incoming_dict[rec.product_id.id] = incoming_dict.get(rec.product_id.id, 0) + rec.quantity
            if rec.location_id == self.location_id:
                outgoing_dict[rec.product_id.id] = outgoing_dict.get(rec.product_id.id, 0) + rec.quantity

        record_list = []
        for res in search:
            in_com = incoming_dict.get(res.product_id.id, 0)
            out_go = outgoing_dict.get(res.product_id.id, 0)
            balance = in_com - out_go
            vals = {
                'product': res.product_id.name,
                'default_code': res.product_id.default_code,
                'uom': res.product_uom_id.name,
                'reference': res.reference,
                'initial_stock': 0,
                'in': in_com,
                'out': out_go,
                'balance': balance,
                'rec_set': res,
            }
            record_list.append(vals)

        category_dict = {}
        for rec_list in record_list:
            category_name = rec_list['rec_set'].product_id.categ_id.name
            category_dict.setdefault(category_name, []).append(rec_list)

        locations = (
            self.read()[0]['location_id'] and self.read()[0]['location_id'][1]
        ) or self.env['stock.location'].search([]).mapped('name')

        start_date_display = self._convert_to_user_timezone(start_date_utc)
        end_date_display = self._convert_to_user_timezone(end_date_utc)

        data = {
            'report_start_date': start_date_display,
            'report_end_date': end_date_display,
            'report_company_id': self.read()[0]['company_id'][1],
            'report_location': locations,
        }

        if self.group_by_category:
            data['search_record'] = category_dict
        else:
            data.update({
                'report_group_by_category': self.read()[0]['group_by_category'],
                'search_record': record_list,
            })

        return self.env.ref('stock_report_cr.action_report_stock_report').report_action(self, data=data)

    # -------------------------------------------------------------------------
    # XLSX Export
    # -------------------------------------------------------------------------
    def button_export_xlsx(self):
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        sheet = workbook.add_worksheet('Inventory Excel Report')

        StockMoveLine = self.env['stock.move.line']

        # Domain setup
        if not self.products:
            domain = [('date', '>=', self.start_date), ('date', '<=', self.end_date)]
            if self.location_id:
                domain.append(('location_dest_id', 'in', self.location_id.ids))
        else:
            domain = [
                ('date', '>=', self.start_date), ('date', '<=', self.end_date),
                ('product_id', 'in', self.products.ids)
            ]
            if self.location_id:
                domain.append(('location_dest_id', 'in', self.location_id.ids))

        # ✅ Using _read_group
        version_count_per_product = dict(
            StockMoveLine._read_group(
                domain=domain,
                groupby=['product_id'],
                aggregates=['id:count'],
            )
        )

        product_ids = [p.id for p in version_count_per_product.keys()]
        if not product_ids:
            return

        all_search = StockMoveLine.search([('product_id', 'in', product_ids)])
        search, product_list = [], []
        for each_item in all_search:
            if each_item.product_id.id not in product_list:
                search.append(each_item)
            product_list.append(each_item.product_id.id)

        move_lines = StockMoveLine.search([])
        incoming_dict, outgoing_dict = {}, {}
        for rec in move_lines:
            if rec.location_dest_id == self.location_id:
                incoming_dict[rec.product_id.id] = incoming_dict.get(rec.product_id.id, 0) + rec.quantity
            if rec.location_id == self.location_id:
                outgoing_dict[rec.product_id.id] = outgoing_dict.get(rec.product_id.id, 0) + rec.quantity

        record_list = []
        for res in search:
            in_com = incoming_dict.get(res.product_id.id, 0)
            out_go = outgoing_dict.get(res.product_id.id, 0)
            balance = in_com - out_go
            vals = {
                'product': res.product_id.name,
                'default_code': res.product_id.default_code,
                'uom': res.product_uom_id.name,
                'reference': res.reference,
                'initial_stock': 0,
                'in': in_com,
                'out': out_go,
                'balance': balance,
                'rec_set': res,
            }
            record_list.append(vals)

        category_dict = {}
        for rec_list in record_list:
            category_name = rec_list['rec_set'].product_id.categ_id.name
            category_dict.setdefault(category_name, []).append(rec_list)

        # Excel Formatting
        header_style = workbook.add_format({'bold': True, 'align': 'center'})
        date_style = workbook.add_format({'align': 'center', 'num_format': 'dd-mm-yyyy'})
        head_style = workbook.add_format({'align': 'center', 'bold': True, 'bg_color': '#dedede'})
        categ_style = workbook.add_format({'bg_color': '#dedede', 'align': 'center'})
        data_font_style = workbook.add_format({'align': 'center'})

        sheet.write(0, 0, 'Warehouse', header_style)
        sheet.write(2, 0, 'Location', header_style)
        sheet.write(4, 0, 'Start Date', header_style)
        sheet.write(6, 0, 'End Date', header_style)
        sheet.write(0, 1, self.company_id.name, date_style)
        sheet.write(2, 1, self.location_id.name, date_style)
        sheet.write(4, 1, self.start_date, date_style)
        sheet.write(6, 1, self.end_date, date_style)

        sheet.set_column('A2:D5', 27)
        row_head = 8
        sheet.write(row_head, 0, 'Reference', head_style)
        sheet.write(row_head, 1, 'Designation', head_style)
        sheet.write(row_head, 2, 'UoM', head_style)
        sheet.write(row_head, 3, 'Initial stock', head_style)
        sheet.write(row_head, 4, 'IN', head_style)
        sheet.write(row_head, 5, 'OUT', head_style)
        sheet.write(row_head, 6, 'Balance', head_style)
        sheet.freeze_panes(10, 0)

        row = 10
        if self.group_by_category:
            for main in category_dict:
                sheet.write(row, 0, main, categ_style)
                for i in range(1, 7):
                    sheet.write(row, i, '', categ_style)
                for line in category_dict[main]:
                    row += 1
                    sheet.write(row, 0, '', data_font_style)
                    if line.get('default_code'):
                        sheet.write(row, 0, line.get('default_code'), data_font_style)
                    sheet.write(row, 1, line.get('product'), data_font_style)
                    sheet.write(row, 2, line.get('uom'), data_font_style)
                    sheet.write(row, 3, line.get('initial_stock'), data_font_style)
                    sheet.write(row, 4, line.get('in'), data_font_style)
                    sheet.write(row, 5, line.get('out'), data_font_style)
                    sheet.write(row, 6, line.get('balance'), data_font_style)
                row += 2
        else:
            for line in record_list:
                row += 1
                sheet.write(row, 0, '', data_font_style)
                if line.get('default_code'):
                    sheet.write(row, 0, line.get('default_code'), data_font_style)
                sheet.write(row, 1, line.get('product'), data_font_style)
                sheet.write(row, 2, line.get('uom'), data_font_style)
                sheet.write(row, 3, line.get('initial_stock'), data_font_style)
                sheet.write(row, 4, line.get('in'), data_font_style)
                sheet.write(row, 5, line.get('out'), data_font_style)
                sheet.write(row, 6, line.get('balance'), data_font_style)
        row += 2

        workbook.close()
        xlsx_data = output.getvalue()
        self.xls_file = base64.encodebytes(xlsx_data)
        self.xls_filename = "Stock Excel Report.xlsx"

        return {
            'type': 'ir.actions.act_url',
            'name': 'Inventory Excel Report',
            'url': '/web/content/stock.reports/%s/xls_file/%s?download=true' % (
                self.id, 'Stock Excel Report.xlsx'),
        }
