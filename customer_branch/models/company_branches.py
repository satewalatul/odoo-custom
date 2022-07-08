from odoo import fields, models


class CompanyBranches(models.Model):
    _name = "customer.branches"
    _description = "Customer Branches"

    name = fields.Char(string='Branch Name', required=True)
    vat = fields.Char(string="GSTIN")

    # Billing Address
    billing_street = fields.Char(string="Billing Address", required=True)
    billing_street2 = fields.Char(string="Billing Address Line 2")
    billing_state_id = fields.Many2one("res.country.state", string='Billing State', ondelete='restrict',
                                       domain="[('country_id', '=', billing_country_id)]")
    billing_country_id = fields.Many2one('res.country', string='Billing Country', ondelete='restrict')
    billing_zip = fields.Char(string='Billing Pincode', change_default=True)

    # Delivery Address
    delivery_street = fields.Char(string="Delivery Address", required=True)
    delivery_street2 = fields.Char(string="Delivery Address Line 2")
    delivery_state_id = fields.Many2one("res.country.state", string='Delivery State', ondelete='restrict',
                                        domain="[('country_id', '=', delivery_country_id)]")
    delivery_country_id = fields.Many2one('res.country', string='Delivery Country', ondelete='restrict')
    delivery_zip = fields.Char(string='Delivery Pincode', change_default=True)

    partner_id = fields.Many2one("res.partner", "Company")
