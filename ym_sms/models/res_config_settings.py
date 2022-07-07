# -*- coding: utf-8 -*-

from odoo import models, fields

class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    api_key = fields.Char(string='Api Key', config_parameter='ym_sms.api_key')
    url = fields.Char(string='SMS Endpoint', config_parameter='ym_sms.url')
    sender = fields.Char(string='Sender', config_parameter='ym_sms.sender')

    sales_head_contact = fields.Char(string='Sales Team Head', size=10, config_parameter='ym_sms.sales_head_contact')
    accounts_head_contact = fields.Char(string='Accounts Team Head', size=10, config_parameter='ym_sms.accounts_head_contact')
    ops_head_contact = fields.Char(string='Ops Team Head', size=10, config_parameter='ym_sms.ops_head_contact')
