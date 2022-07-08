from odoo import fields, models


class Company(models.Model):
    _inherit = "res.partner"
    _description = 'Branches'

    branch_ids = fields.One2many('customer.branches', string='Branches', inverse_name='partner_id')
