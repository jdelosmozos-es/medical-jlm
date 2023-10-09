from odoo import models, api

class Lead(models.Model):
    _inherit='crm.lead'
        
    @api.model_create_multi
    def create(self, vals_list):
        import sys;sys.path.append(r'/home/javier/.var/app/org.eclipse.Java/eclipse/plugins/org.python.pydev.core_10.2.1.202307021217/pysrc')
        import pydevd;pydevd.settrace('127.0.0.1',port=9999)
        Partner = self.env['res.partner']
        for vals in vals_list:
            if 'user_id' in vals and 'partner_id' in vals:
                if vals['user_id'] not in Partner.browse(vals['partner_id']).authorized_users:
                    Partner.browse(vals['partner_id']).write({'authorized_users': [(4,vals['user_id'],0)]})
        return super(Lead, self).create(vals_list)
    
    def write(self, vals):
        for record in self:
            if record.user_id and record.partner_id:
                Ver qué pasa si antes no tenía alguno de los dos y ahora sí y al revés.
                Poner es igual que crear.
                Para quitar tengo que comprobar todo lo del usuario. Debería ser un método del usuario, porque puede depender de otros modelos (paciente)
        return super(Lead, self).write(vals)