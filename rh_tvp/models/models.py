# -*- coding: utf-8 -*-

from odoo import api, _, tools, fields, models, exceptions, SUPERUSER_ID
from odoo.exceptions import AccessError, UserError, RedirectWarning, ValidationError, Warning
from datetime import datetime, date, time
from dateutil.relativedelta import relativedelta


class RHFields(models.Model):
    _inherit = 'hr.employee'

    antiquity = fields.Char(string='Antigüedad', compute='_antiquity_calculation')
    antiquity_years = fields.Integer(string='Antigüedad Años', compute='_compute_years')
    date_in = fields.Date(string='Fecha de Ingreso')
    date_out = fields.Date(string='Fecha de Baja')
    reason = fields.Selection(
        [('1', 'Renuncia'), ('2', 'Recorte de Personal'), ('3', 'Fin de Contrato'), ('4', 'Otro')],
        string='Motivo de Baja')
    commnets = fields.Text(string='Comentarios')
    month_in = fields.Selection([(1, '01'), (2, '02'), (3, '03'), (4, '04'),
                                 (5, '05'), (6, '06'), (7, '07'), (8, '08'),
                                 (9, '09'), (10, '10'), (11, '11'), (12, '12')], string='Mes de Entrada', store=True,
                                compute="_month_in")
    month_born = fields.Selection([(1, '01'), (2, '02'), (3, '03'), (4, '04'),
                                   (5, '05'), (6, '06'), (7, '07'), (8, '08'),
                                   (9, '09'), (10, '10'), (11, '11'), (12, '12')], string='Mes de Compleaños',
                                  store=True, compute="_month_born")
    imss = fields.Char(string="IMSS")
    vat_tvp = fields.Char(string="RFC")
    curp_tvp = fields.Char(string="CURP")
    depto_name = fields.Char(string='Nombre del Departamento')

    @api.onchange('department_id')
    def _onchange_name_depto(self):
        if self.department_id:
            self.depto_name = self.department_id.name

    @api.one
    @api.depends('date_in', 'month_in')
    def _month_in(self):
        if self.date_in:
            self.month_in = datetime.strptime(str(self.date_in), '%Y-%m-%d').strftime('%m')

    @api.one
    @api.depends('birthday', 'month_born')
    def _month_born(self):
        if self.birthday:
            self.month_born = datetime.strptime(str(self.birthday), '%Y-%m-%d').strftime('%m')

    @api.one
    @api.depends('date_in', 'date_out', 'antiquity', 'active')
    def _antiquity_calculation(self):
        if self.active == True:
            if self.date_in:
                diff = relativedelta(datetime.today(), datetime.strptime(str(self.date_in), '%Y-%m-%d'))
                years = diff.years
                months = diff.months
                days = diff.days
                self.antiquity = '{} Años {} Meses {} Dias'.format(years, months, days)
        else:

            if self.date_out and self.date_in:
                datein = fields.Datetime.from_string(self.date_in)
                dateout = fields.Datetime.from_string(self.date_out)
                diff = relativedelta(dateout, datein)
                years = diff.years
                months = diff.months
                days = diff.days
                self.antiquity = '{} Años {} Meses {} Dias'.format(years, months, days)

    @api.multi
    @api.depends('date_in', 'antiquity_years')
    def _compute_years(self):
        for record in self:
            if record.date_in and record.date_in <= fields.Date.today():
                record.antiquity_years = relativedelta(
                    fields.Date.from_string(fields.Date.today()),
                    fields.Date.from_string(record.date_in)).years
            else:
                record.antiquity_years = 0

class HrContact(models.Model):
    _inherit = 'hr.contract'

    contract_company = fields.Many2one('res.partner', string='Empresa Contratante')
    anual_base = fields.Selection([('1', '1'), ('2', '12.5'), ('3', '14'), ('4', '16'), ('5', '17')],
                                  string='Base Anual')
    salary_biweekly = fields.Float(string='Salario Quincenal', compute="_salary_biweekly")
    salary_annual = fields.Float(string='Salario Anual', compute="_salary_annual")
    date_low = fields.Date(string="Fecha de Baja")
    reason_low = fields.Selection(
        [('1', 'Contrato Vencido'), ('2', 'Renuncia Voluntaria'), ('3', 'Renovacion de Contrato'),
         ('4', 'Cambio de puesto o departamento'), ('5', 'Recorte de Personal')], string="Motivo de baja del contrato")
    settlement = fields.Float(string="Monto Finiquitado")
    commnets = fields.Text(string="Comentarios")

    @api.one
    @api.depends('anual_base', 'salary_annual', 'wage')
    def _salary_annual(self):
        if self.anual_base == '1':
            self.salary_annual = self.wage * 1
        if self.anual_base == '2':
            self.salary_annual = (self.wage * 12.5)
        if self.anual_base == '3':
            self.salary_annual = (self.wage * 14)
        if self.anual_base == '4':
            self.salary_annual = (self.wage * 16)
        if self.anual_base == '5':
            self.salary_annual = (self.wage * 17)

    @api.one
    @api.depends('salary_biweekly', 'wage')
    def _salary_biweekly(self):
        self.salary_biweekly = (self.wage / 2)

class leavefields(models.Model):
    _inherit = 'hr.leave.type'

    validity = fields.Integer(string='Vigencia en meses', default=18)
    days = fields.Integer(string='Dias')
    antiquity_years = fields.Integer(string='Antigüedad')


class leaveasignations(models.Model):
    _inherit = 'hr.leave.allocation'

    antiquity = fields.Integer(string='Antigüedad Años')
    validity = fields.Integer(string='Vigencia en meses', default=18)
    date_in = fields.Date(string='Fecha de Ingreso')
    antiquity_years_allocation = fields.Integer(related='holiday_status_id.antiquity_years', string='')
    comple_laboral = fields.Date(string='Cumpleaños Laboral', compute='_cumple_laboral_calcution')
    vencimiento = fields.Date(string='Vencimiento', compute='_cumple_laboral_calcution')
    unusable_days = fields.Boolean(string='Dias no utilizables',default=False, compute='_unusable_days_function')
    extended_permission = fields.Boolean(string='Permiso Extendido', default=False)

    @api.onchange('employee_id')
    def _onchange_antiquity(self):
        if self.employee_id:
            self.antiquity = self.employee_id.antiquity_years
            self.date_in = self.employee_id.date_in

    @api.onchange('holiday_status_id')
    def _onchange_days(self):
        if self.holiday_status_id:
            self.number_of_days_display = self.holiday_status_id.days

    @api.one
    @api.depends('date_in', 'comple_laboral', 'antiquity', 'validity')
    def _cumple_laboral_calcution(self):
        if self.date_in:
            self.comple_laboral = fields.Date.from_string(self.date_in) + relativedelta(years=self.antiquity)
            self.vencimiento = fields.Date.from_string(self.comple_laboral) + relativedelta(months=self.validity)
    @api.one
    def _unusable_days_function(self):
        today = fields.Date.from_string(fields.Date.today())
        if self.vencimiento:
            if today > self.vencimiento:
                self.unusable_days = True


class issues_leaves(models.Model):
    _inherit = 'hr.leave'

    days_before_approval = fields.Integer(string="Saldo de días antes de la aprobación")
    unusable_days = fields.Boolean(string='Dias no utilizables', compute='_holyday', store=True)
    extended_permission = fields.Boolean(string='Permiso Extendido', compute='_holyday', store=True)
    expiration = fields.Date(string="Fecha de Vencimiento", compute='_holyday', store=True)
    days_to_expiration = fields.Char(string="Tiempo de Expiracion", compute='_message_error', store=True)

    @api.onchange('holiday_status_id')
    def _onchange_days_before_approval(self):
        if self.holiday_status_id:
            self.days_before_approval = self.holiday_status_id.virtual_remaining_leaves

    @api.one
    @api.depends('holiday_status_id')
    def _holyday(self):
        for rec in self:
            if rec.holiday_status_id:
                res = self.env['hr.leave.allocation'].search([('holiday_status_id', '=', self.holiday_status_id.id)])
                rec.unusable_days = res.unusable_days
                rec.extended_permission = res.extended_permission
                rec.expiration = res.vencimiento

    @api.multi
    @api.depends('expiration','unusable_days','extended_permission')
    def _message_error(self):
        if self.unusable_days == True and self.extended_permission == False:
            raise UserError(_('Los dias dentro de esta categoria se encuentran vencidos, consulta con tu administrador'))

        if self.expiration:
            today = fields.Date.from_string(fields.Date.today())
            dateout = fields.Date.from_string(self.expiration)
            diff = relativedelta(dateout, today)
            years = diff.years
            months = diff.months
            days = diff.days
            self.days_to_expiration = '{} Años {} Meses {} Dias'.format(years, months, days)


