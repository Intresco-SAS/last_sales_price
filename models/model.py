# -*- coding: utf-8 -*-

from odoo import models, fields, api


class SalesOrderLine(models.Model):

    _inherit = 'sale.order.line'

    last_sales_price = fields.Float(string='Ultimo Precio Venta', compute='_compute_last_sales_price')

    def _compute_last_sales_price(self):
        move_line_obj = self.env['account.move.line'].sudo()
        for line in self:
            line.last_sales_price = 0
            if line and line.product_id and line.order_id and line.order_id.partner_id:
                invoice_line = move_line_obj.search([
                    ('product_id', '=', line.product_id.id),
                    ('move_id.move_type', '=', 'out_invoice'),
                    ('move_id.partner_id', '=', line.order_id.partner_id.id),
                ], order='id desc', limit=1)
                if invoice_line:
                    line.last_sales_price = invoice_line.price_unit

    @api.onchange('order_id.partner_id', 'product_id')
    def _onchange_data_change(self):
        self._compute_last_sales_price()


class AccountMoveLine(models.Model):

    _inherit = 'account.move.line'

    last_sales_price = fields.Float(string='Ultimo Precio Venta', compute='_compute_last_sales_price')

    def _compute_last_sales_price(self):
        move_line_obj = self.env['account.move.line'].sudo()
        for line in self:
            line.last_sales_price = 0
            if type(line.id) is int:
                if line and line.product_id and line.move_id and line.move_id.partner_id:
                    invoice_line = move_line_obj.search([
                        ('id', '!=', line.id),
                        ('product_id', '=', line.product_id.id),
                        ('move_id.move_type', '=', 'out_invoice'),
                        ('move_id.partner_id', '=', line.move_id.partner_id.id),
                    ], order='id desc', limit=1)
                    if invoice_line:
                        line.last_sales_price = invoice_line.price_unit

    @api.onchange('move_id.partner_id', 'product_id')
    def _onchange_data_change(self):
        self._compute_last_sales_price()
