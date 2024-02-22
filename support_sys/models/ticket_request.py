from odoo import models, fields, api
from datetime import datetime


class Ticket(models.Model):
    _name = 'ticket.request'
    _description = 'Ticket Request'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'ticket_ref'

    ticket_ref = fields.Char(readonly=1, default=lambda self: 'New', string='Ticket ID')
    ticket_type = fields.Many2one('ticket.type',string='Ticket Type')
    company_service_category_id = fields.Many2one('company.service.category')
    client_id = fields.Many2one('res.partner',string='Requested By')
    project = fields.Char(string='Project')
    subject = fields.Char(string='Subject', required=True)
    priority = fields.Selection([('0', 'Low'),('1','Wishlist'),('2', 'Medium'),('3', 'High'),('4', 'Urgent')],
                                string='Priority', tracking=True)
    issue = fields.Char(string='Issue Description', required=True)
    state = fields.Selection(
        [('New', 'New'), ('On Progress', 'On Progress'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')],
        default='New', String="Progress", required=True, tracking=True)
    issue_supporting_document = fields.Binary(string='Supporting Doc', tracking=True)
    notes = fields.Text('Additional Info')

    # this is for assigning the ticket request to employee
    assigning_remarks = fields.Char('Remarks',tracking=True)
    assigned_deadline = fields.Date("Assigned Deadline",tracking=True)
    assigned_department = fields.Many2one('hr.department',string="Assigned Department",tracking=True)
    assigned_employee = fields.Many2one('hr.employee',string="Assigned Employee",tracking=True)


    @api.model
    def create(self,vals):
        vals['ticket_ref'] = self.env['ir.sequence'].next_by_code("ticket.request.code")
        return super(Ticket, self).create(vals)


    def action_cancelled(self):
        self.state = 'Cancelled'

    def action_in_progress(self):
        self.state = 'On Progress'

    def action_in_completed(self):
        self.state = 'Completed'

    def action_assign_employee(self):
        return {
            'name': 'Enter Details',
            'type':'ir.actions.act_window',
            'res_model':'assign.ticket.wizard.model',
            'view_mode':'form',
            'view_id':self.env.ref('support_sys.view_assign_ticket_popup').id,
            'target':'new',
            'context':{
                'default_ticket_request_id':self.id
            }
        }   
class AllowDurationPopup(models.TransientModel):
    _name = 'assign.ticket.wizard.model'
    _description = "Assign Ticket Transient Model"

    
    # this is for assigning the ticket request to employee
    ticket_request_id = fields.Many2one('ticket.request')
    assigning_remarks = fields.Char('Remarks')
    assigned_deadline = fields.Date("Assigned Deadline")
    assigned_department = fields.Many2one('hr.department',string="Assigned Department")
    assigned_employee = fields.Many2one('hr.employee',string="Assigned Employee")

    def assign_ticket_to_employee(self):
        self.env['ticket.request'].search([('id','=',self.ticket_request_id.id)]). write({
            'assigning_remarks':self.assigning_remarks,
            'assigned_deadline':self.assigned_deadline,
            'assigned_department':self.assigned_department.id,
            'assigned_employee':self.assigned_employee.id
        })
    
    # def update_counter_offer_price(self):
    #     print(f"This is the value of the duration count {self.duration_count}")
    #     print(f"This is the value of the leave request id {self.leave_request_id.id}")
    #     self.env['leave.request'].search([('id','=',self.leave_request_id.id)]).write({
    #         'allowed_duration':self.duration_count,
    #         'start_date_ad':self.leave_start_date,
    #         'end_date_ad':self.leave_end_date
    #     })
        
        
class TicketType(models.Model):
    _name = 'ticket.type'
    _description = 'Ticket Type'

    name = fields.Char('Ticket Type')

# class TicketRaise(models.Model):
#     _name = 'ticket.raise'
#     _description = 'Ticket Type'

#     name = fields.Char('Ticket Type')

class CompanyProvidedServiceCategory(models.Model):
    _name = 'company.service.category'
    _description = 'Company Service Category'

    name = fields.Char('Company Service Type')
        # ticket_type = fields.Selection(
        # [('complain', 'Complain'), ('feedback', 'Feedback'), ('request', 'Request'), ('query', 'Query')],
        # string='Ticket Type', tracking=True)