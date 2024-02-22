from odoo import models,fields,api

state_selection_items = [
    ('draft','Draft'),
    ('approved','Approved'),
    ('declined','Declined'),
]

class AdvanceRequest(models.Model):
    _name = 'advance.request'
    _description= 'Advance request'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    employee_id = fields.Many2one('hr.employee',"Employee")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    requested_amount = fields.Float('Advance Requested Amount')
    expense_type = fields.Many2one('expense.type')
    date_from = fields.Datetime('Start Date')
    date_to = fields.Datetime('End Date')
    file_upload = fields.Binary('Supporting Documents')
    advance_request_reason = fields.Text('Advance Request Reason')
    state = fields.Selection(selection=state_selection_items,default="draft",string='State')
    notes = fields.Text('Additional Info')

    def action_accepted(self):
        self.write({'status': 'approved'})

    def action_rejected(self):
        self.write({'status': 'declined'})

class ExpenseType(models.Model):
    _name = 'expense.type'
    _description = 'Expense Type'

    name = fields.Char('Expense Type')



class ExpenseRequest(models.Model):
    _name = 'expense.request'
    _description = 'Employee Expense Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']


    # Employee Info
    employee_id = fields.Many2one('hr.employee','Employee')

    # Client Info
    project_id = fields.Many2many('company.project', string='Project')
    serviced_client_id = fields.Many2many('client.info',string='Serviced Client')
    branch_id = fields.Many2one('branch.info',string='Branch Id')

    # Expense Info
    expense_type = fields.Many2many('expense.type',string="Expense Type")
    expense_description = fields.Text(string='Expense Description', required=True)
    expense_start_date = fields.Date("Expense Start Date")
    expense_end_date = fields.Date("Expense End Date")
    currency_id = fields.Many2one('res.currency', string='Currency', required=True)
    amount = fields.Float(string='Amount', required=True)
    
    # Expense Location
    starting_location = fields.Char(string='Starting Location', tracking=True)
    ending_location = fields.Char(string='Ending Location', tracking=True)

    # Additional Info
    receipt_attachment = fields.Binary(string='Receipt Attachment', attachment=True)
    notes = fields.Text(string='Notes')
    
    # State
    state = fields.Selection(selection=state_selection_items,default="draft",string='State')

    def action_accepted(self):
        self.write({'status': 'approved'})

    def action_rejected(self):
        self.write({'status': 'declined'})

    # def submit_ticket(self):
    #     return {'type': 'ir.actions.act_window_close'}

    
    # stay_name = fields.Char("Hotel Name")
    # hotel_address = fields.Char("Address", tracking=True)
    # hotel_phone = fields.Char("Phone", tracking=True)

        

    
class ClientType(models.Model):
    _name = 'client.type'

    name = fields.Char("Client Type")
    
    
class CompanyProjects(models.Model):
    _name = 'company.project'

    company_service_category_id = fields.Many2one('company.service.category',string="Company Service Category")
    name = fields.Char("Project Name")
