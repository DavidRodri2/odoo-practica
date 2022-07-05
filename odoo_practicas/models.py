from logging import exception
from operator import truediv
from odoo import models, fields, api

class res_partner(models.Model):
    _name='res.partner'
    _inherit = 'res.partner'
    company_type = fields.Selection(selection_add=[('is_school','Escuela')])
    
class academia_student (models.Model):
    _name = "academia.student"
    _description = "Modelo para formulación de estudiantes"
    name = fields.Char('Nombre', size = 128, required = True)
    last_name =fields.Char('Apellido', size = 128)
    photo = fields.Binary('Fotografía')
    create_date = fields.Datetime('Fecha de creación',readonly=True)
    create_date = fields.Html('Comentarios')
    note = fields.Boolean('Activo')
    curp = fields.Char('curp', size = 18)
    state = fields.Selection([('draft','Documento borrador'),
                                ('process', 'Proceso'),
                                ('done','Egresado',)],'Estado',default='draft')
    
    partner_id = fields.Many2one('res.partner','Escuela')
    calificaciones_id = fields.One2many(
        'academia.calificacion',
        'student_id',
        'Calificaciones'
    )
    
 
    @api.constrains('curp')
    def _check_lines(self):
        if len(self.curp) < 18:
            raise exception.ValidationError('Curp debe tener 18 caracteres')
        
    age = fields.Integer('Edad')
    _order = 'name'
    active = fields.Boolean("Activo", default=True)
    
    
    
    
