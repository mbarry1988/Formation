# -*- coding: utf-8 -*-


from odoo import models, fields, api

class ExtPartner(models.Model):
     _inherit = 'res.partner'

     sexe = fields.Selection([('masculin','Masculin'),('feminin','Féminin')],string="Sexe")
     age = fields.Float (string="Age")
     show = fields.Boolean(string="Afficher")
