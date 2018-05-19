# -*- coding: utf-8 -*-


from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Session(models.Model):
     _name = 'openacademy.session'

     name = fields.Char(string="Nom de la session")
     date_start = fields.Date(string="Date début", default=fields.Date.today)
     date_stop = fields.Date(string="Date de Fin", default=fields.Date.today)
     duration = fields.Float(string="Durée")
     seats = fields.Integer(string="Nombre de places")
     instructeur_id = fields.Many2one('res.partner', string="Instructeur")
     cours_id = fields.Many2one('openacademy.course', string="Cours", required=True)
     participant_ids = fields.Many2many('res.partner', string="Participants")
     taken_seats = fields.Float(string="Pourcentage de places occupées", compute='_taken_seats')
     valide = fields.Boolean(string='Valide')
     nbre_participant = fields.Integer(string="Nombre de participant",compute='_nb_participant',store=True)
     statut = fields.Selection([('ouvrir','Ouvert'),('fermer','Fermer')],string="Statut")

     @api.depends('participant_ids')
     def _nb_participant(self):
          for r in self:
               r.nbre_participant=len(r.participant_ids)

     def valid_session(self):
          for r in self:
               print("+++++++++++++++++++++++++++++++++++")
               r.valide = True

     @api.onchange('seats','participant_ids')
     def _verify_valid_seats(self):
          if self.seats < 0:
               return {
                    'warning': {
                         'title': "incorrect 'seats' value",
                         'message': "The number of available seats may not be negative",
                    },
               }
          if self.seats < len(self.participant_ids):
               return {
                    'warning': {
                         'title': "Too many attendees",
                         'message': "Increase seats or remove excess attendees",
                    },
               }

     @api.depends('seats','participant_ids')
     def _taken_seats(self):
          for r in self:
               if not r.seats:
                    r.taken_seats = 0.0
               else:
                    r.taken_seats = 100.0*len(r.participant_ids)/r.seats

     @api.constrains('participant_ids')
     def _verify_age(self):
          for r in self:
               for participant in r.participant_ids:
                    print('====',self,r,participant,r.participant_ids)
                    if participant.age > 30:
                         raise ValidationError(" l'age du  participant %s est %s L'age dépasse la limite de 30 ans" % (participant.name ,participant.age))