# -*- coding: utf-8 -*-
import json

from odoo import models, fields, api, _

import logging
import requests
from odoo import api, models
import traceback
from datetime import datetime

from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)


class SaleOrderInherit(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    jobsite_id = fields.Many2one(
        'jobsite', string='Site Name', index=True, tracking=10,
        help="Linked site (optional). You can find a site by its Name.")

    #
    # @api.depends('tentative_quo')
    # def _compute_partner_id_domain_tentative(self):
    #     for rec in self:
    #         if rec.tentative_quo:
    #             new_domain = json.dumps(['|', '&', ('is_company', '=', True), '&', ('is_customer_branch', '=', False), (rec.tentative_quo, '=', False), '&', ('is_customer_branch', '=', False),  (rec.tentative_quo, '=', True)])
    #             rec.partner_id_domain_tentative = new_domain
    #         else:
    #             new_domain = json.dumps([('is_company', '=', True), ('is_customer_branch', '=', False)])
    #             rec.partner_id_domain_tentative = new_domain
    #
    #
    # partner_id_domain_tentative = fields.Char(compute="_compute_partner_id_domain_tentative", readonly=True, store=False)
    tentative_quo = fields.Boolean('Tentative Quotation', default=False)
    partner_id = fields.Many2one(comodel_name='res.partner', domain="['|', '&', ('is_company', '=', True), '&', ('is_customer_branch', '=', False), ('rec.tentative_quo', '=', False), '&', ('is_customer_branch', '=', False),  ('rec.tentative_quo', '=', True)]")

    customer_branch = fields.Many2one(comodel_name='res.partner', string='Customer Branch', domain="[('is_company', "
                                                                                                   "'=', True), "
                                                                                                   "('is_customer_branch', '=', True), ('parent_id', '=', partner_id)]")


    @api.model
    def _get_default_country(self):
        country = self.env['res.country'].search([('code', '=', 'IN')], limit=1)
        return country

    po_number = fields.Char(string="PO Number")

    # Billing Address
    billing_street = fields.Char(string="Billing Address")
    billing_street2 = fields.Char()
    billing_state_id = fields.Many2one("res.country.state", string='Billing State', ondelete='restrict',
                                       domain="[('country_id', '=', billing_country_id)]")
    billing_country_id = fields.Many2one('res.country', string='Billing Country', ondelete='restrict',
                                         default=_get_default_country)
    billing_zip = fields.Char(string='Billing Pincode', change_default=True)

    # Delivery Address
    delivery_street = fields.Char(string="Delivery Address")
    delivery_street2 = fields.Char()
    delivery_state_id = fields.Many2one("res.country.state", string='Delivery State', ondelete='restrict',
                                        domain="[('country_id', '=', delivery_country_id)]")
    delivery_country_id = fields.Many2one('res.country', string='Delivery Country', ondelete='restrict',
                                          default=_get_default_country)
    delivery_zip = fields.Char(string='Delivery Pincode', change_default=True)

    pickup_date = fields.Date('Pickup Date')

    #jobsite_godowns = fields.Boolean(related='jobsite_id.godown_ids', store=False)
    godown = fields.Many2one("jobsite.godown", string='Godown', ondelete='restrict')

    delivery_date = fields.Date('Delivery Date')
    security_amount = fields.Float(string="Security Amount")
    freight_amount = fields.Float(string="Freight Amount", default=0.0)
    freight_paid_by = fields.Selection([
        ('freight_type1', 'It has been agreed 1st Dispatch and final Pickup will be done by Youngman'),
        ('freight_type2',
         'It has been agreed 1st Dispatch will be done by Youngman and final Pickup will be done by Customer on his '
         'cost'),
        ('freight_type3',
         'It has been agreed 1st Dispatch will be done by Customer on his cost and final Pickup would be done by '
         'Youngman'),
        ('freight_type4',
         'It has been agreed 1st Dispatch will be done by Customer on his cost and final Pickup is already paid by '
         'Customer'),
        ('freight_type5', 'It has been agreed 1st Dispatch and final Pickup will be done by Customer on his cost')],
        string="Freight To Be Paid By : ",
        default='freight_type1')

    price_type = fields.Selection([
        ('daily', 'Daily'),
        ('monthly', 'Monthly')],
        string="Price Type",
        default='monthly')
    purchaser_name = fields.Many2one("res.partner", string='Purchaser Name',
                                     domain="[('parent_id', '=', customer_branch),('category_id','ilike','purchaser'),('is_company','=', False)]")
    purchaser_phone = fields.Char(string='Purchaser Contact Phone')
    purchaser_email = fields.Char(string='Purchaser Email')
    below_min_price = fields.Boolean('Below Min Price', default=False)

    otp = fields.Integer(string='OTP', store=False)
    otp_verified = fields.Boolean(string='OTP', store=False, default=False)  # TODO compute field should be equal to



    is_security_letter = fields.Boolean(related='customer_branch.security_letter', store=False)
    is_rental_advance = fields.Boolean(related='customer_branch.rental_advance', store=False)
    is_rental_order = fields.Boolean(related='customer_branch.rental_order', store=False)
    is_security_cheque = fields.Boolean(related='customer_branch.security_cheque', store=False)


    security_letter = fields.Binary('Security Letter')
    rental_advance = fields.Binary('Rental Advance')
    rental_order = fields.Binary('Rental Order')
    security_cheque = fields.Binary('Security Cheque')


    def action_confirm(self):
        if self.po_number is None or (self.security_letter is None and self.customer_branch.security_letter is True):
            raise ValidationError(_('Testing'))

        res = super(SaleOrderInherit, self).action_confirm()


    @api.onchange('purchaser_name')
    def get_purchaser_phone(self):
        if self.purchaser_name:
            self.purchaser_phone = self.purchaser_name.phone
            self.purchaser_email = self.purchaser_name.email

    @api.onchange('jobsite_id')
    def get_delivery_address(self):
        if self.jobsite_id:
            self.delivery_street = self.jobsite_id.street
            self.delivery_street2 = self.jobsite_id.street2
            self.delivery_state_id = self.jobsite_id.state_id
            self.delivery_country_id = self.jobsite_id.country_id
            self.delivery_zip = self.jobsite_id.zip

    @api.onchange('partner_id')
    def clear_customer_branch(self):
        if self.partner_id:
            self.customer_branch = False
            self.billing_street = False
            self.billing_street2 = False
            self.billing_state_id = False
            self.billing_zip = False
            self.billing_country_id = False

    @api.onchange('customer_branch')
    def get_billing_address(self):
        if self.customer_branch:
            self.billing_street = self.customer_branch.street
            self.billing_street2 = self.customer_branch.street2
            self.billing_state_id = self.customer_branch.state_id
            self.billing_zip = self.customer_branch.zip

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
