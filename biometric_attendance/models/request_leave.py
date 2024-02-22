from odoo import models,fields

class LeaveRequest(models.Model):
    _name = 'leave.permission'
    
    name = fields.Char()