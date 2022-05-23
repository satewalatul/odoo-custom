from odoo import api, fields, models

class CrmLead(models.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'

    site_id = fields.Many2one(
        'jobsite', string='Job Site', index=True, tracking=10,
        help="Linked site (optional). You can find a site by its Name.")