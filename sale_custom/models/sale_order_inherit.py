# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
from odoo import api, models

_logger = logging.getLogger(__name__)


class SaleOrderInherit(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    jobsite_id = fields.Many2one(
        'jobsite', string='Site Name', required=True, index=True, tracking=10,
        help="Linked site (optional). You can find a site by its Name.")
    billing_address = fields.Char(string="Billing Address", required=True)
    state_id = fields.Many2one("res.country.state", string='Billing State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Billing Country', ondelete='restrict')
    zip = fields.Char(string='Pincode', change_default=True)
    pickup_date = fields.Date('Pickup Date', required=True)
    delivery_date = fields.Date('Delivery Date', required=True)
    security_amount = fields.Float(string="Security Amount", required=True)
    freight_amount = fields.Float(string="Freight Amount", required=True, default=0.0)
    freight_paid_by = fields.Selection([
        ('paid_by_1', 'It has been agreed 1st Dispatch & Final Pickup will be done by Youngman')],
        string="Freight To Be Paid By : ",
        required=True, default='paid_by_1')
    price_type = fields.Selection([
        ('daily', 'Daily'),
        ('monthly', 'Monthly')],
        string="Price Type",
        required=True, default='daily')
    below_min_price = fields.Boolean('Below Min Price', default=False)
    otp = fields.Integer(string='OTP')

    def verify_otp(self):
        return

    def request_otp(self):
        return

class ProductTemplateInherit(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    list_price = fields.Float('Rental Price', digits='Product Price', required=True, default=0.0)
    standard_price = fields.Float(
        'Estimate Value', company_dependent=True,
        digits='Product Price',
        groups="base.group_user",
    )


# class SaleOrderLineInherit(models.Model):
#     _inherit = 'sale.order.line'
#     _description = 'sale.order.line'
#
#     @api.onchange('price_unit')
#     def min_price(self):
#         if self.order_id.below_min_price:
#             return
#
#         product_id = self.product_id
#         unit_price = self.env['product.product'].search([('id', '=', product_id.id)], limit=1).list_price
#         current_price = self.price_unit
#         if current_price < unit_price:
#             self.price_unit = self._origin.price_unit
#             return {
#                 'warning': {'title': 'Warning',
#                             'message': 'Current Price < Unit Price', },
#             }
