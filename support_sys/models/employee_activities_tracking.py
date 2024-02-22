from odoo import models, fields, api
from datetime import datetime


class EmployeeTaskAssignment(models.Model):
    _name = 'employee.task.assignment'
    _description = 'Employee Task Assignment'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True,tracking=True)
    task_name = fields.Char(string='Task Name', required=True,tracking=True)
    assigned_project_id = fields.Many2many('company.project',string="Assigned Project",tracking=True)
    assigned_location = fields.Char('Location',tracking=True)
    client_id = fields.Many2one('client.info', string='Client', required=True,tracking=True)
    start_date = fields.Date('Assigned Date',tracking=True)
    deadline = fields.Date(string='Deadline',tracking=True)
    notes = fields.Text("Notes")
    department=fields.Many2one('hr.department',string="Departments")
    department_id=fields.Integer(related='department.id')
    completed_date=fields.Date('Completed Date',tracking=True)
    status=fields.Selection([('onprogress','On Progress'),('completed','Completed')],string="Status",default='onprogress',tracking=True)
    @api.onchange('client_id')
    def onchange_client_id(self):
        pass


class EmployeeDailyReport(models.Model):
    _name = 'employee.daily.work.report'
    _description = 'Employee Daily Work Report'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    employee_id = fields.Many2one('hr.employee',string='Employee',tracking=True)
    work_type = fields.Many2one('employee.work.type',string='Work Type',tracking=True)
    work_date = fields.Date(string="Work Date",tracking=True)
    task_detail = fields.Text(string='Task Detail',tracking=True)
    start_time = fields.Char('Start Time',tracking=True)
    end_time = fields.Char('End Time',tracking=True)
    hours_worked = fields.Float(string='Hours Worked',compute="calculate_worked_hour",tracking=True,store=True)
    additional_notes = fields.Text(string='Additional Notes',tracking=True)
    client_id=fields.Many2one('client.info',string="Client Id")
    branch_id=fields.Many2one('branch.info',string="Branch")
    project_id=fields.Many2one('company.project',string="Project")
    is_organization = fields.Boolean(string='Is Organization', related='client_id.is_organization', store=True)
    supporting_docs=fields.Many2many('ir.attachment',string="Supporting Docs")

    @api.depends('start_time','end_time')
    def calculate_worked_hour(self):
        for rec in self:
            if (rec.start_time and rec.end_time):
                hours, minutes = map(int, rec.start_time.split(':'))
                total_start_seconds = hours * 3600 + minutes * 60
                converted_start_time = float(total_start_seconds)
                hours2, minutes2 = map(int, rec.end_time.split(':'))
                total_end_seconds = hours2 * 3600 + minutes2 * 60
                converted_end_time = float(total_end_seconds)
                rec.hours_worked = (converted_end_time - converted_start_time) / 3600


class EmployeeWorkType(models.Model):
    _name = 'employee.work.type'
    _description = 'Employee Work Type'
    _rec_name = 'work_type'


    work_type = fields.Char('Work Type')

