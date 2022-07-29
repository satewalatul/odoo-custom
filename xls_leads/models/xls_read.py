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

        client = pygsheets.authorize(service_account_file='custom/xls_leads/models/keys.json')
        sheet1 = client.open_by_url('')
        worksheet = sheet1.sheet1
        cells = worksheet.get_all_values(include_tailing_empty_rows=False, include_tailing_empty=False,
                                         returnas='matrix')
        end_row = len(cells)
        indices = {
            'TIMESTAMP': 0,
            'NAME': 1,
            'COMPANY': 2,
            'REQUIREMENT': 3,
            'DESIGNATION': 4,
            'BRANCH': 5,
            'NAME_NUMBER': 6,
            'NUMBER': 7,
            'STATUS': 8,
            'ID': 9

        }
        leads = [{
            'create_date': new_lst[indices['TIMESTAMP']],
            'contact_name': new_lst[indices['NAME']],
            'partner_name': new_lst[indices['COMPANY']],
            'name': new_lst[indices['REQUIREMENT']],
            #'designation': new_lst[indices['DESIGNATION']],
            'branch': new_lst[indices['BRANCH']], #to do
            'lead_qual': new_lst[indices['NAME_NUMBER']], #to do
            'number': new_lst[indices['NUMBER']],
            'status': new_lst[indices['STATUS']], #to do
            #'id': new_lst[indices['ID']]

        } for new_lst in cells[2:]]
        print(leads)
        #worksheet.delete_rows(8, number=5) //TO DELETE ROWS
        for lead in leads:
            try:
                self.env['crm.lead'].create(lead)
            except:
                tb =traceback.format_exc()
                _logger.error(tb)
                pass


