from odoo import models, fields, api, _

class Partner(models.Model):
    _inherit = 'res.partner'
    
    is_patient = fields.Boolean(compute='_compute_patient')
    
    @api.depends('name')
    def _compute_patient(self):
        for record in self:
            search = self.env['medical.patient'].search(['|',
                                    ('partner','=',record.id),
                                    '|',
                                    ('couple_member_1.partner','=',record.id),
                                    ('couple_member_2.partner','=',record.id),
                            ])
            if search:
                record.is_patient = True
            else:
                record.is_patient = False
                
    def action_show_patient(self):
        self.ensure_one()
        patients = self.env['medical.patient'].search(['|',
                                    ('partner','=',self.id),
                                    '|',
                                    ('couple_member_1.partner','=',self.id),
                                    ('couple_member_2.partner','=',self.id),
                            ])
        result = {
            "type": "ir.actions.act_window",
            "res_model": "medical.patient",
            "domain": [('id', 'in', patients.ids)],
            "context": {"create": False},# 'default_move_type': 'in_invoice'},
            "name": _("Patients"),
            'view_mode': 'tree,form',
        }
        return result
    