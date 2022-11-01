from odoo import models, fields, api, exceptions

class academia_materia_list(models.Model):
    _name = 'academia.materia.list'
    grado_id = fields.Many2one('academia.grado', 'ID Referencia')
    materia_id = fields.Many2one('academia.materia', 'Materia', required=True)

class academia_grado(models.Model):
    _name = 'academia.grado'
    _description = 'Modelo Grados con un listado de materias'

    name = fields.Selection([
        ('1', 'Primero'),
        ('2', 'Segundo'),
        ('3', 'Tercero'),
        ('4', 'Cuarto'),
        ('5', 'Quinto'),
        ('6', 'Sexto')],
        'Grado', required=True)
    grupo = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('c', 'C'),
    ], 'Grupo')
    materia_ids = fields.One2many(
        'academia.materia.list', 'grado_id', 'Materias')


class res_partner(models.Model):
    _inherit = 'res.partner'
    company_type = fields.Selection(
        selection_add=[('is_school', 'Escuela'), ('student', 'Estudiante')])
    student_id = fields.Many2one(
        'academia.student',
        'Estudiante')
    property_payment_term_id = fields.Many2one('account.payment.term', company_dependet=True,
                                               string='Customer Payment Terms',
                                               help='This payment terms will be used instead of the default one for sale order')
    property_supplier_payment_term_id = fields.Many2one('account.payment.term', company_dependet=True,
                                                        string='Vendor Payment Terms',
                                                        help="This payment terms will be used instead of the default one for purchase orders and")

class academia_student (models.Model):
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _name = 'academia.student'
    _description = 'Modelo de formulario para estudiantes'

    @api.depends('calificaciones_id')
    def calcula_promedio(self):
        acum = 0.0  
        if len(self.calificaciones_id) > 0:
            for xcal in self.calificaciones_id:
                acum += xcal.calificacion
                if acum:
                    self.promedio = acum/len(self.calificaciones_id)
        else:
            self.promedio = 0.0

    @api.depends('invoice_ids')
    def calcula_amount(self):
        acum = 0.0
        for xcal in self.invoice_ids:
            acum += xcal.amount_total
        if acum:
            self.amount_invoice = acum

    def _get_school_default(self):
        school_id = self.env['res.partner'].search(
            [('name', '=', 'Escuela_comodin')])
        return school_id

    _name = "academia.student"
    _description = "Modelo para formulación de estudiantes"
    name = fields.Char('Nombre', size=128, required=True,
                       track_visibility='onchange')
    last_name = fields.Char('Apellido', size=128, track_visibility='onchange')
    photo = fields.Binary('Fotografía')
    create_date = fields.Datetime('Fecha de creación', readonly=True)
    note = fields.Html('Comentarios')
    active = fields.Boolean('Activo')
    age = fields.Integer('Edad', required=True, track_visibility='onchange')
    curp = fields.Char('curp', size=18, copy=False)
    state = fields.Selection([('draft', 'Documento borrador'),
                              ('process', 'Proceso'),
                              ('done', 'Egresado',)],
                             'Estado', default='draft')

    partner_id = fields.Many2one(
        'res.partner', 'Escuela', default=_get_school_default)
    calificaciones_id = fields.One2many(
        'academia.calificacion',
        'student_id',
        'Calificaciones')

    country = fields.Many2one('res.country', 'Pais',
                              related='partner_id.country_id')
    invoice_ids = fields.Many2many('account.invoice',
                                   'student_invoice_rel',
                                   'student_id', 'invoice_id',
                                   'Facturas')

    grado_id = fields.Many2one('academia.grado', 'Grado')

    promedio = fields.Float('Promedio', digits=(14, 2),
                            compute="calcula_promedio")
    amount_invoice = fields.Float(
        'Monto Facturado', digits=(14, 2), compute='calcula_amount')

    @api.constrains('curp')
    def _check_lines(self):
        if len(self.curp) < 18:
            raise exceptions.ValidationError('Curp debe tener 18 caracteres')

    
    def write(self, values):
        if 'curp' in values:
            values.update({
                'curp': values['curp'].upper()
            })
        result = super(academia_student, self).write(values)
        return result

    def create(self, values):
        if values['name']:
            nombre = values['name']
            exist_ids = self.env['academia.student'].search(
                [('name', '=', self.name)])
            if exist_ids:
                values.update({
                    'name': values['name']+"(copia)",
                })
        res = super(academia_student, self).create(values)
        partner_obj = self.env['res.partner']
        vals_to_partner = {
            'name': res['name']+" "+res['last_name'],
            'company_type': 'student',
            'student_id': res['id'],
        }
        print(vals_to_partner)
        partner_id = partner_obj.create(vals_to_partner)
        print("===>partner_id", partner_id)
        return res

    
    def unlink(self):
        partner_obj = self.env['res.partner']
        partner_ids = partner_obj.search([('student', 'in', self.ids)])
        print("Partner ##### >>>>>", partner_ids)
        if partner_ids:
            for partner in partner_ids:
                partner.unlink()
        res = super(academia_student, self).unlink()
        return res

    
    def confirm(self):
        self.state = 'process'
        return True

    
    def done(self):
        self.state = 'done'
        return True

    
    def cancel(self):
        self.state = 'cancel'
        return True

    
    def draft(self):
        self.state = 'draft'
        return True

    age = fields.Integer('Edad')
    _order = 'name'
    active = fields.Boolean("Activo", default=True)
