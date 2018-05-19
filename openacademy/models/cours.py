# -*- coding: utf-8 -*-


from odoo import models, fields, api

class Cours(models.Model):
     _name = 'openacademy.course'

     _sql_constraints = [('name_unique', 'UNIQUE(name)', 'Le Nom est unique')]

     name = fields.Char(string="Nom du cours")
     description = fields.Text(string="Description")
     remarque = fields.Text(string="Remarque")
     user_id = fields.Many2one ('res.users',string = "Responsable")
     session_ids = fields.One2many ('session.course','cours_id', string="Sessions")
     active_2 = fields.Boolean(string="Actif")
     etat = fields.Selection([('brouillon','Brouillon'),('encours','En Cours'),('termine','terminé')],string="Etat")


     @api.model
     def create(self, vals):
          obj = super(Cours, self).create(vals)
          cours_sequence = self.env['ir.sequence']
          obj.name = cours_sequence.next_by_code('openacademy.course')
          print(obj)
          return obj

     @api.multi
     def etat_encours(self):
          for r in self:
               r.write({'etat':'encours'})

     @api.multi
     def etat_terminer(self):
          for r in self:
               r.write({'etat':'termine'})

     @api.multi
     def etat_brouillon(self):
          for r in self:
               if r.active_2:
                    cours_obj = self.env['openacademy.course']
                    cours_ids = cours_obj.search([('active_2','=',True)])
                    session_obj = self.env['openacademy.session']
                    session_ids = session_obj.search([])
                    for session in session_ids:
                         session.valid_session()
                         print(session,session.name)
                         session.seats = 10

                    r.etat="brouillon"

     def active_cours(self):
          print('==========================',self)
          cours_ids = self.env['openacademy.course'].search([])
          print('=====',cours_ids)
          for cours in cours_ids:
               cours.active_2 = not cours.active_2




class Session_Cours(models.Model):
     _name = 'session.course'

     session_id = fields.Many2one('openacademy.session', string="Session")
     description = fields.Text(string="Description")
     cours_id = fields.Many2one ('openacademy.course', string="Cours")
