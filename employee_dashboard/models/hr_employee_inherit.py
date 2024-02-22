from odoo import models,fields,api

class EmployeeInherit(models.Model):
    _inherit ='hr.employee'
    # _rec_name='employee_ref'

    contract=fields.Binary(string="Contract")

    employee_ref = fields.Char(readonly=1, default=lambda self: 'New', string='Employee ID')
    language_spoken=fields.Char(string="Language Spoken")
    permanent_address=fields.Char(string="Permanent Address")
    temporary_address=fields.Char(string="Temporary Address")
    age=fields.Integer(string="Age")
    bank_account_no=fields.Char(string="Bank Account Number")
    bank_name=fields.Char(string="Bank  Name")
    account_name=fields.Char(string=" Account Name")
    # family
    father_name=fields.Char(string="Fathers Name")
    mother_name=fields.Char(string="Mothers Name")
    partner_name=fields.Char(string="Partner Name")
    grandfather_name=fields.Char(string="GrandFathers Name")

    #Citizenship Info
    nationality=fields.Char(string="Nationality")
    issued_place=fields.Char(string="Issued Place")
    identification_file=fields.Binary(string="Identification Docs")
    upload_pan=fields.Binary(string="Pan File")
    pan=fields.Char(string="PAN No.")
    # Education Info
    education_ids = fields.One2many('employee.education', 'employee_id', string='Education')

    # work experience
    work_experience_ids = fields.One2many('employee.work.experience', 'employee_id', string='Work Experience')

    # emergency contact
    emergency_contact_id=fields.One2many('employee.emergency.contact','employee_id',string="Emergency Contact")

    # work related info
    professional_certifications=fields.Binary(string="Professional Certificates")
    related_skills=fields.Char(string="Skills")
    training_taken=fields.Char(string="Training")
    position=fields.Char(string="Postion")
    cv=fields.Binary(string="CV")
    cover_letter = fields.Binary(string="Cover Letter")
    training_certificates=fields.Many2many('ir.attachment',string="Training Certificate")

    # @api.model
    # def create(selfself,vals):
    #     vals['employee_ref']=