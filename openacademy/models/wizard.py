# -*- coding: utf-8 -*-


from odoo import models, fields, api


class Wizard(models.TransientModel):
     _name = 'openacademy.wizard'


     def _default_session(self):
         return self.env['openacademy.session'].browse(self._context.get('active_id'))


     session_id = fields.Many2one('openacademy.session', string="Session", required=True, default=_default_session)
     attendee_ids = fields.Many2many('res.partner', string="Attendees")

     @api.multi
     def subscribe(self):
         print("=====",self.attendee_ids)
         self.session_id.participant_ids |= self.attendee_ids
         print("===========",self.session_id.participant_ids)
         return {}