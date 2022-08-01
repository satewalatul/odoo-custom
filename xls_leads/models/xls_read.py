from __future__ import print_function
import json
import traceback
from google.oauth2 import service_account
from google.auth.transport.requests import AuthorizedSession
from odoo import fields, models, api
import pygsheets

import logging

_logger = logging.getLogger(__name__)



class ReadXls(models.TransientModel):
    _name = 'cron.xls'

    @api.model
    def cron_test(self):
        print("checking")
        print("Executing")

        # secret_dict = {
        #         "type": self.env['ir.config_parameter'].sudo().get_param('xls_leads.type'),
        #         "project_id": self.env['ir.config_parameter'].sudo().get_param('xls_leads.project_id'),
        #         "private_key_id": self.env['ir.config_parameter'].sudo().get_param('xls_leads.private_key_id'),
        #         "client_email": self.env['ir.config_parameter'].sudo().get_param('xls_leads.client_email'),
        #         "client_id": self.env['ir.config_parameter'].sudo().get_param('xls_leads.client_id'),
        #         "auth_uri": self.env['ir.config_parameter'].sudo().get_param('xls_leads.auth_uri'),
        #         "token_uri": self.env['ir.config_parameter'].sudo().get_param('xls_leads.token_uri'),
        #         "auth_provider_x509_cert_url": self.env['ir.config_parameter'].sudo().get_param('xls_leads.auth_provider_x509_cert_url'),
        #         "client_x509_cert_url": self.env['ir.config_parameter'].sudo().get_param('xls_leads.client_x509_cert_url')
        #     }
        # SCOPES = ('https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive')
        # s1 = json.dumps(secret_dict)
        # service_account_info = json.loads(s1)
        # my_credentials = service_account.Credentials.from_service_account_info(service_account_info, scopes=SCOPES)
        # client = pygsheets.authorize(custom_credentials=my_credentials)

        client = pygsheets.authorize(service_account_file='odoo-custom/xls_leads/models/keys.json')
        sheet1 = client.open_by_url('https://docs.google.com/spreadsheets/d/1joEMBnP87NFMrB0N11C0SzqvKYmn0CxKYv4hvQh2yUA')
        worksheet = sheet1.sheet1
        cells = worksheet.get_all_records(empty_value='', head=1, majdim='ROWS')



        end_row = len(cells)
        leads = [{
            'contact_name': lead['customer_name'],
            'partner_name': lead['customer_company'],
            'name': lead['customer_requirement'],
            'phone': lead['customer_number'],
            'lead_qual': lead['your_name'],
            'lead_qual_num': lead['your_number']
        } for lead in cells]
        print(leads)

        for lead in leads:
            try:
                self.env['crm.lead'].create(lead)
            except:
                tb =traceback.format_exc()
                _logger.error(tb)
                pass
        # worksheet.delete_rows(2, number=end_row)

