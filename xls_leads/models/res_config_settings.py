# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    type = fields.Char(string='type', config_parameter='xls_leads.type')
    project_id = fields.Char(string='project_id', config_parameter='xls_leads.project_id')
    private_key_id = fields.Char(string='private_key_id', config_parameter='xls_leads.private_key_id')
    client_email = fields.Char(string='client_email', config_parameter='xls_leads.client_email')
    client_id = fields.Char(string='client_id', config_parameter='xls_leads.client_id')
    auth_uri = fields.Char(string='auth_uri', config_parameter='xls_leads.auth_uri')
    token_uri = fields.Char(string='token_uri', config_parameter='xls_leads.token_uri')
    auth_provider_x509_cert_url = fields.Char(string='auth_provider_x509_cert_url', config_parameter='xls_leads.auth_provider_x509_cert_url')
    client_x509_cert_url = fields.Char(string='token_uri', config_parameter='xls_leads.client_x509_cert_url')
