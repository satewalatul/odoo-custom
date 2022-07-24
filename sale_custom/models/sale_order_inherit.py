# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
import requests
from odoo import api, models
import traceback
from datetime import datetime

_logger = logging.getLogger(__name__)


class SaleOrderInherit(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    jobsite_id = fields.Many2one(
        'jobsite', string='Site Name', required=True, index=True, tracking=10,
        help="Linked site (optional). You can find a site by its Name.")

    # Billing Address
    billing_street = fields.Char(string="Billing Address", required=True)
    billing_street2 = fields.Char()
    billing_state_id = fields.Many2one("res.country.state", string='Billing State', ondelete='restrict',
                                       domain="[('country_id', '=', billing_country_id)]")
    billing_country_id = fields.Many2one('res.country', string='Billing Country', ondelete='restrict')
    billing_zip = fields.Char(string='Billing Pincode', change_default=True)

    # Delivery Address
    delivery_street = fields.Char(string="Delivery Address", required=True)
    delivery_street2 = fields.Char()
    delivery_state_id = fields.Many2one("res.country.state", string='Delivery State', ondelete='restrict',
                                        domain="[('country_id', '=', delivery_country_id)]")
    delivery_country_id = fields.Many2one('res.country', string='Delivery Country', ondelete='restrict')
    delivery_zip = fields.Char(string='Delivery Pincode', change_default=True)

    pickup_date = fields.Date('Pickup Date', required=True)
    godown = fields.Many2one("jobsite", string='Godown', ondelete='restrict',
                             domain="[('id', '=', jobsite_id)]")

    delivery_date = fields.Date('Delivery Date', required=True)
    security_amount = fields.Float(string="Security Amount", required=True)
    freight_amount = fields.Float(string="Freight Amount", required=True, default=0.0)
    freight_paid_by = fields.Selection([
        ('freight_type1', 'It has been agreed 1st Dispatch and final Pickup will be done by Youngman'),
        ('freight_type2',
         'It has been agreed 1st Dispatch will be done by Youngman and final Pickup will be done by Customer on his cost'),
        ('freight_type3',
         'It has been agreed 1st Dispatch will be done by Customer on his cost and final Pickup would be done by Youngman'),
        ('freight_type4',
         'It has been agreed 1st Dispatch will be done by Customer on his cost and final Pickup is already paid by Customer'),
        ('freight_type5', 'It has been agreed 1st Dispatch and final Pickup will be done by Customer on his cost')],
        string="Freight To Be Paid By : ",
        required=True, default='freight_type1')
    price_type = fields.Selection([
        ('daily', 'Daily'),
        ('monthly', 'Monthly')],
        string="Price Type",
        required=True, default='monthly')
    purchaser_phone = fields.Char(string='Purchaser Contact Phone', required=True)
    purchaser_name = fields.Many2one("res.partner", string='Purchaser Name',
                                     domain="[('parent_id', '=', partner_id),('category_id','ilike','purchaser'),('phone','ilike',purchaser_phone)]")
    purchaser_email = fields.Many2one("res.partner", string='Purchaser Email',
                                      domain="[('parent_id', '=', partner_id),('category_id','ilike','purchaser'),('phone','ilike',purchaser_phone)]")
    below_min_price = fields.Boolean('Below Min Price', default=False)
    otp = fields.Integer(string='OTP', store=False)
    otp_verified = fields.Boolean(string='OTP', store=False, default=False)  # TODO compute field should be equal to

    @api.onchange('jobsite_id')
    def get_delivery_address(self):
        if (self.jobsite_id != False):
            self.delivery_street = self.jobsite_id.street
            self.delivery_street2 = self.jobsite_id.street2
            self.delivery_state_id = self.jobsite_id.state_id
            self.delivery_country_id = self.jobsite_id.country_id
            self.delivery_zip = self.jobsite_id.zip

    @api.onchange('branch_id')
    def get_billing_address(self):
        if (self.branch_id != False):
            self.billing_street = self.branch_id.billing_street
            self.billing_street2 = self.branch_id.billing_street2
            self.billing_state_id = self.branch_id.billing_state_id
            self.billing_country_id = self.branch_id.billing_country_id
            self.billing_zip = self.branch_id.billing_zip

    def verify_otp(self):
        otp = self._generate_otp()
        if self.otp == otp:
            self.below_min_price = True
            # self.otp_verified = True
            return {
                'warning': {'title': 'OTP Verified',
                            'message': 'OTP has been verified.', },
            }
        else:
            return {
                'warning': {'title': 'Warning',
                            'message': 'OTP did not match. Please try again.', },
            }

    def request_otp(self):
        api_key = self.env['ir.config_parameter'].sudo().get_param('ym_sms.api_key')
        endpoint = self.env['ir.config_parameter'].sudo().get_param('ym_sms.url')
        sender = self.env['ir.config_parameter'].sudo().get_param('ym_sms.sender')
        number = self.env['ir.config_parameter'].sudo().get_param('ym_sms.sales_head_contact')

        otp = self._generate_otp()

        url = "%s?apikey=%s&text=OTP:- %s Youngman India Pvt. Ltd.&mobileno=%s&sender=%s" % (
        endpoint, api_key, str(otp), number, sender)

        try:
            response = requests.request("POST", url, headers={}, data={})
            response.raise_for_status()
        except requests.exceptions.HTTPError as err:
            tb = traceback.format_exc()
            _logger.error(tb.print_exc())
            return {
                'warning': {'title': 'Warning',
                            'message': 'Could not send OTP', },
            }

        return {
            'info': {'title': 'Warning',
                     'message': 'Could not send OTP', },
        }

    def _generate_otp(self):
        now = datetime.now()

        code = now.year * now.month * now.day * now.hour * now.minute
        code = str(code * 1000000)

        return code[:6]


class ItemsCategory(models.Model):
    _name = 'items.category'
    _description = "Items Category"
    name = fields.Char(string='Category')

class ProductTemplateInherit(models.Model):
    _name = 'product.template'
    _inherit = 'product.template'

    status = fields.Selection([
        ('0', 'ACTIVE'),
        ('1', 'DEACTIVE'),
        ('2', 'DISABLE'),
    ], string='Status')

    bundle = fields.Boolean(default=False, string="Bundle")
    consumable = fields.Boolean(default=False, string="Consumable")
    serialized = fields.Boolean(default=False, string="Serialized")
    list_price = fields.Float('Rental Price', digits=(12, 2), required=True, default=0.0)
    meters = fields.Float('Meters', default=0.0)
    length = fields.Float('Length (inch)', default=0.0)
    breadth = fields.Float('Breadth (inch)', default=0.0)
    height = fields.Float('Height (inch)', default=0.0)
    actual_weight = fields.Float('Actual Weight (kg)', default=0.0)
    vol_weight = fields.Float('Volume Weight', default=0.0)
    cft = fields.Float('CFT (cu ft)', default=0.0)
    missing_estimate_value = fields.Float('Missing Estimate Value', digits=(12, 2), default=0.0)
    material = fields.Text(string="Material")
    item_type = fields.Char(string="Item Type")
    purchase_code = fields.Char(string="Purchase Code")
    supplier = fields.Char(string="Supplier")
    category = fields.Many2one(comodel_name='items.category', string='Category')
    standard_price = fields.Float(
        'Estimate Value', company_dependent=True, digits=(12, 2),
        groups="base.group_user",
    )


class SaleOrderLineInherit(models.Model):
    _inherit = 'sale.order.line'
    _description = 'sale.order.line'

    item_code = fields.Char(string="Item Code")

    @api.onchange('price_unit')
    def min_price(self):
        if self.order_id.below_min_price:
            return

        product_id = self.product_id
        unit_price = self.env['product.product'].search([('id', '=', product_id.id)], limit=1).list_price
        current_price = self.price_unit
        if current_price < unit_price:
            self.price_unit = self._origin.price_unit
            return {
                'warning': {'title': 'Warning',
                            'message': 'Current Price < Unit Price', },
            }
