from odoo import models, fields, api


class EmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    task_type = fields.Many2many('employee.work.type', string="Task Type")
    project = fields.Many2many('company.project', string="Project")
    client = fields.Many2many('client.info', string="Client")
