from logging import exception
from odoo import models, fields, api, exceptions

class academia_calificacion(models.Model):
    _name="academia.calificacion"
    _description = "Calificaciones"
    
     
    name = fields.Many2one('academia.materia', 'Materia')
    calificacion=fields.Float('Calificacion', digits=(3,2))
    student_id =fields.Many2one('academia.student','ID Ref')
    
    
    @api.constrains('calificacion')
    def _check_calificacion(self):
        if self.calificacion < 5 or self.calificacion > 10:
            raise exceptions.ValidationError("Calificacion debe ser mayor a 5 y menor a 10")
     
class academia_materia(models.Model):
    _name = "academia.materia"
    _description = "Materias"
    name = fields.Char('Nombre')
    
    
    _sql_constraints=[('name_uniq','unique(name)',
        'El nombre de la materia debe ser único')]
    
    
    