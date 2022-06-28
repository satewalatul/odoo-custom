# -*- coding: utf-8 -*-

from odoo import models, fields, api

import logging
from odoo import api, models

_logger = logging.getLogger(__name__)

class SaleOrderInherit(models.Model):
    _name = 'sale.order'
    _inherit = 'sale.order'

    jobsite_id = fields.Many2one(
        'jobsite', string='Site Name', required=True, index=True, tracking=10, help="Linked site (optional). You can find a site by its Name.")

