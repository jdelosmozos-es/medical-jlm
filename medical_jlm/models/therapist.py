from odoo import models, fields

class Therapist(models.Model):
    _name = 'medical.therapist'
    _inherits = {'res.partner': 'partner'}
    _description = 'Model to manage therapist information.'
    
    partner = fields.Many2one(comodel_name='res.partner', required=True, ondelete='restrict')
#    agenda
    therapies = fields.Many2many(comodel_name='medical.therapist.therapy')
    patients = fields.One2many(comodel_name='medical.patient', inverse_name='therapist')
    description = fields.Text()
    
class Therapy(models.Model):
    _name = 'medical.therapist.therapy'
    _description = 'Type of therapy'
    
    name = fields.Char(required=True)
    description = fields.Text()