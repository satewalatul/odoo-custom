from odoo import api, fields, models, tools, _

class SaleOrder(models.Model):
    _inherit = "sale.order"

    branch_id = fields.Many2one('customer.branches', string='Branch', domain="[('partner_id','=',partner_id)]")
    
