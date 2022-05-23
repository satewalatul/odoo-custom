# -*- coding: utf-8 -*-

from odoo import models, fields, api
from random import randint
import logging
from odoo import api, fields, models, _

from odoo.exceptions import ValidationError

_logger = logging.getLogger(__name__)

class PartnerInherit(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    def _default_channel_tag(self):
        return self.env['res.partner.channel.tag'].browse(self._context.get('channel_tag_id'))

    def _default_bd_tag(self):
        return self.env['res.partner.bd.tag'].browse(self._context.get('bd_tag_id'))

    in_beta = fields.Boolean(default=False, string="In Beta")

    channel_tag_ids = fields.Many2many('res.partner.channel.tag', column1='partner_id',
                                   column2='channel_tag_id', string='Channel Tags', default=_default_channel_tag)
    bd_tag_ids = fields.Many2many('res.partner.bd.tag', column1='partner_id',
                                       column2='bd_tag_id', string='BD Tags', default=_default_channel_tag)

    bd_tag_user_ids = fields.One2many('contact.team.users', 'contact_id', string='Contact Team Users', help="Users having this BD Tag as team name")

    @api.onchange('bd_tag_ids')
    def _onchange_bd_tag_ids(self):
        _logger.error("called _onchange_bd_tag_ids")
        _logger.error(str(self.id) + " has " + str(len(self.bd_tag_user_ids)))
        if(self._origin.id):
            self._cr.execute('delete from contact_team_users where contact_id = %s', [self._origin.id])
            _logger.error(str(self.id) + " has " + str(len(self.bd_tag_user_ids)))

            for bd_tag in self.bd_tag_ids:
                users = self.env['res.users'].sudo().search(['|', ('sale_team_id.name', 'ilike', bd_tag.name), ('groups_id.name','=','User: All Documents')])
                _logger.error("For tag name " + str(bd_tag.name) + " " + str(len(users)) + " type " + str(type(self.bd_tag_user_ids)))
                for user in users:
                    self._cr.execute('insert into contact_team_users (user_name, user_id, contact_id) values(%s, %s, %s)', ( user.name, user.id ,self._origin.id))

    @api.onchange('user_id')
    def _onchange_salesperson(self):
        new_user_id = self.user_id
        linked_contacts = self.child_ids
        _logger.error("called _onchange_user_id")
        for contact in linked_contacts:
            _logger.error("updating res_partner user id = " + str(new_user_id.id) + " for user " + str(contact._origin.id))
            self._cr.execute('update res_partner set user_id = %s where id = %s', (new_user_id.id, contact._origin.id))

    @api.onchange('team_id')
    def _onchange_salesteam(self):
        new_team_id = self.team_id
        linked_contacts = self.child_ids
        _logger.error("called _onchange_team_id")
        for contact in linked_contacts:
            _logger.error("updating res_partner team id = " + str(new_team_id.id) + " for user " + str(contact._origin.id))
            self._cr.execute('update res_partner set team_id = %s where id = %s', (new_team_id.id, contact._origin.id))

    @api.onchange('property_payment_term_id')
    def _onchange_property_payment_term_id(self):
        new_payment_term = self.property_payment_term_id
        linked_contacts = self.child_ids
        _logger.error("called _onchange_property_payment_term_id")
        for contact in linked_contacts:
            _logger.error("updating " + contact.name)
            contact.property_payment_term_id = new_payment_term


    @api.model
    def view_header_get(self, view_id, view_type):
        if self.env.context.get('channel_tag_id'):
            return _(
                'Partners: %(channel)s',
                channel=self.env['res.partner.channel.tag'].browse(self.env.context['channel_tag_id']).name,
            )
        if self.env.context.get('bd_tag_id'):
            return _(
                'Partners: %(bd_tag_id)s',
                bd_tag_id=self.env['res.partner.bd.tag'].browse(self.env.context['bd_tag_id']).name,
            )
        return super().view_header_get(view_id, view_type)


class ContactTeamUsers(models.Model):
    _description = 'Contact Team Users'
    _name = 'contact.team.users'

    user_name = fields.Char(string = "User Name")
    user_id = fields.Integer(string = "User Id")
    contact_id = fields.Many2one('res.partner', string="Contact")

class PartnerChannelTag(models.Model):
    _description = 'Partner Channel'
    _name = 'res.partner.channel.tag'
    _order = 'name'
    _parent_store = True

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string='Channel Name', required=True, translate=True)
    color = fields.Integer(string='Color', default=_get_default_color)
    parent_id = fields.Many2one('res.partner.channel.tag', string='Parent Channel', index=True, ondelete='cascade')
    child_ids = fields.One2many('res.partner.channel.tag', 'parent_id', string='Child Channels')
    active = fields.Boolean(default=True, help="The active field allows you to hide the channel without removing it.")
    parent_path = fields.Char(index=True)
    partner_ids = fields.Many2many('res.partner', column1='channel_tag_id', column2='partner_id', string='Partners')

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You can not create recursive tags.'))

    def name_get(self):
        """ Return the channels' display name, including their direct
            parent by default.

            If ``context['partner_channel_display']`` is ``'short'``, the short
            version of the channel name (without the direct parent) is used.
            The default is the long version.
        """
        if self._context.get('partner_channel_display') == 'short':
            return super(PartnerChannelTag, self).name_get()

        res = []
        for channel in self:
            names = []
            current = channel
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((channel.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)


class PartnerBdTag(models.Model):
    _description = 'Partner Channel'
    _name = 'res.partner.bd.tag'
    _order = 'name'
    _parent_store = True

    def _get_default_color(self):
        return randint(1, 11)

    name = fields.Char(string='BD Tag Name', required=True, translate=True)
    color = fields.Integer(string='Color', default=_get_default_color)
    parent_id = fields.Many2one('res.partner.bd.tag', string='Parent Bd tag', index=True, ondelete='cascade')
    child_ids = fields.One2many('res.partner.bd.tag', 'parent_id', string='Child Bd tags')
    active = fields.Boolean(default=True, help="The active field allows you to hide the bdtag without removing it.")
    parent_path = fields.Char(index=True)
    partner_ids = fields.Many2many('res.partner', column1='bd_tag_id', column2='partner_id', string='Partners')

    @api.constrains('parent_id')
    def _check_parent_id(self):
        if not self._check_recursion():
            raise ValidationError(_('You can not create recursive tags.'))

    def name_get(self):
        """ Return the channels' display name, including their direct
            parent by default.

            If ``context['partner_channel_display']`` is ``'short'``, the short
            version of the bdtag name (without the direct parent) is used.
            The default is the long version.
        """
        if self._context.get('partner_bdtag_display') == 'short':
            return super(PartnerBdTag, self).name_get()

        res = []
        for bdtag in self:
            names = []
            current = bdtag
            while current:
                names.append(current.name)
                current = current.parent_id
            res.append((bdtag.id, ' / '.join(reversed(names))))
        return res

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        args = args or []
        if name:
            # Be sure name_search is symetric to name_get
            name = name.split(' / ')[-1]
            args = [('name', operator, name)] + args
        return self._search(args, limit=limit, access_rights_uid=name_get_uid)