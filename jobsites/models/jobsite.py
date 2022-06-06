import logging

from odoo import api, fields, models


class Jobsite(models.Model):
    _name = 'jobsite'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'format.address.mixin']
    _description = "Jobsite"

    name = fields.Char(string='Site Name', required=True, translate=True, tracking=True)
    siteteam = fields.Many2one(comodel_name='crm.team', string='Team')

    status = fields.Selection([
        ('Virgin', 'Virgin'),
        ('Active', 'Active'),
        ('Closed', 'Closed'),
    ], string="Status",
        required=True, default='Virgin', help="", tracking=True)
    note = fields.Text(string='Description')
    active = fields.Boolean(string='isActive', default=True, tracking=True)
    street = fields.Char()
    street2 = fields.Char()
    zip = fields.Char(change_default=True)
    city = fields.Char()
    state_id = fields.Many2one("res.country.state", string='State', ondelete='restrict',
                               domain="[('country_id', '=?', country_id)]")
    country_id = fields.Many2one('res.country', string='Country', ondelete='restrict')
    country_code = fields.Char(related='country_id.code', string="Country Code")
    latitude = fields.Float(string='Geo Latitude', digits=(10, 7))
    longitude = fields.Float(string='Geo Longitude', digits=(10, 7))
    marker_color = fields.Char(string='Marker Color', default='red', required=True)
    user_id = fields.Many2one(
        'res.users', string='Salesperson', default=lambda self: self.env.user, index=True, tracking=True)

    @api.model
    def _geo_localize(self, street='', zip='', city='', state='', country=''):
        geo_obj = self.env['base.geocoder']
        search = geo_obj.geo_query_address(
            street=street, zip=zip, city=city, state=state, country=country
        )
        result = geo_obj.geo_find(search, force_country=country)
        if result is None:
            search = geo_obj.geo_query_address(
                city=city, state=state, country=country
            )
            result = geo_obj.geo_find(search, force_country=country)
        return result

    def geo_localize(self):
        for lead in self.with_context(lang='en_US'):
            result = self._geo_localize(
                street=lead.street,
                zip=lead.zip,
                city=lead.city,
                state=lead.state_id.name,
                country=lead.country_id.name,
            )

            if result:
                lead.write(
                    {
                        'latitude': result[0],
                        'longitude': result[1],
                    }
                )

        return True

    # class ResPartner(models.Model):
    #     _inherit = 'res.partner'
    #
    #     marker_color = fields.Char(
    #         string='Marker Color', default='red', required=True)
