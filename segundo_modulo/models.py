from odoo import models, fields, api

class Account_name(models.Model):
    _name = "account.move"
    
    name = fields.Char('Nombre', required=True)
    last_name = fields.Char('Apellido', size=128)
    create_date = fields.Datetime('Fecha de creación', readonly=True)
    active = fields.Boolean('Activo')