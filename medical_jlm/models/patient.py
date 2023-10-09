from odoo import models, fields, api, _
from odoo.exceptions import UserError

class Patient(models.Model):
    _name = 'medical.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Model to manage patient information.'
    
    partner = fields.Many2one(comodel_name='res.partner', ondelete='cascade')
    name = fields.Char()
    therapist = fields.Many2one(comodel_name='medical.therapist', ondelete='set null')
    clinical_information = fields.Html()
    
    is_couple = fields.Boolean(default=False)
    couple_member_1 = fields.Many2one(comodel_name='medical.patient', domain=[('couple','=',False)], ondelete='restrict')
    couple_member_2 = fields.Many2one(comodel_name='medical.patient', domain=[('couple','=',False)], ondelete='restrict')
    
    couple = fields.Many2one(comodel_name='medical.patient', compute='_compute_couple')
    couple_counterpart = fields.Many2one(comodel_name='medical.patient', compute='_compute_couple')
    patient_provided_info = fields.One2many(comodel_name='medical.patient.data', inverse_name='patient', readonly=True)
    tags = fields.Many2many(comodel_name='medical.patient.tag')
    therapy = fields.Many2one(comodel_name='medical.therapist.therapy', ondelete='restrict', domain="[('therapist','=',therapist)]")
    state = fields.Selection(selection=[('initial','Initial'),('active','Active'),('stand_by','Stand by'),('finished','Finished')], default='initial', )
    
    def name_get(self):
        result = []
        for record in self:
            result.append((record.id,record.name if record.is_couple else record.partner.name))
        return result
            
    @api.constrains('is_couple','couple_members','partner')
    def _couple_constraint(self):
        for record in self:
            if record.is_couple and (not record.couple_member_1 or not record.couple_member_2):
                raise UserError(_('One couple should have two members'))
            if record.is_couple and record.partner:
                raise UserError(_('A couple cannot be related to a partner, instead it should have two members.'))
            if not record.is_couple and not record.partner:
                raise UserError(_('A patient must be a person or a couple'))
    
    @api.constrains('partner')
    def _partner_constraint(self):
        for record in self:
            if record.partner.is_company:
                raise UserError(_('A company cannot be a patient.'))
            
    @api.depends('couple')
    def _compute_couple(self):
        for record in self:
            couple = self.env['medical.patient'].search(['|',('couple_member_1','=',record.id),('couple_member_2','=',record.id)])
            if couple:
                record.couple = couple[0]
            else:
                record.couple = False
            if couple:
                if record.couple.couple_member_1 == record:
                    record.couple_counterpart = record.couple.couple_member_2
                else:
                    record.couple_counterpart = record.couple.couple_member_1
            else:
                record.couple_counterpart = False
                
class PatientProvidedData(models.Model):
    _name = 'medical.patient.data'
    _description = 'Data provided by the patient directly'
    
    patient = fields.Many2one(comodel_name='medical.patient')
    date = fields.Date()
    data = fields.Html(string='Information from patient')