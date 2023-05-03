

from odoo import models,_

import logging,requests
import traceback

_logger= logging.getLogger(__name__)


class YmSms(models.TransientModel):
    _name = 'ym.sms'
    _description = 'Send Message To Users'

    def send_sms_to_number(self, mobile_number, message):
        try:
            api_key = self.env['ir.config_parameter'].sudo().get_param('ym_sms.api_key')
            endpoint = self.env['ir.config_parameter'].sudo().get_param('ym_sms.endpoint')
            sender = self.env['ir.config_parameter'].sudo().get_param('ym_sms.sender')

            if not (api_key or endpoint or sender or mobile_number):
                _logger.error("Rapid SMS details not configured. Please reach out to system admins")
                return False

            url = "%s?apikey=%s&text=%s&mobileno=%s&sender=%s" % (endpoint, api_key, message, mobile_number, sender)
            response = requests.request("POST", url, headers={}, data={})
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as err:
            tb = traceback.format_exc()
            _logger.error(tb.print_exc())
            return False


    def send_sms(self,partner_id, message):
            if not (partner_id or message):
                return False
            else:
                number = partner_id.mobile if partner_id.mobile else partner_id.phone if partner_id.phone else False
                return self.send_sms_to_number(number, message)
