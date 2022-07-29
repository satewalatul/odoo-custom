# -*- coding: utf-8 -*-

from odoo import fields, models, api

import logging
_logger = logging.getLogger(__name__)


class CrmLead(models.Model):
    _name = 'crm.lead'
    _inherit = 'crm.lead'

    job_order = fields.Char(string="Job Order")

    lead_qual = fields.Many2one(
        'res.users', string='Lead Qualifier', default=lambda self: self.env.user,
        domain="['&', ('share', '=', False), ('company_ids', 'in', user_company_ids)]",
        check_company=True, index=True, tracking=True)


    branch = fields.Many2one('jobsite.godown', string="Branch")