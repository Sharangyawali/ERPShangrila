from odoo import models, fields, api

class EmployeeRegistrationRequest(models.Model):
    _name = 'employee.registration.request'
    _description = 'Employee Registration Request'
    _rec_name='registration_ref'

    # Personal
    registration_ref = fields.Char(readonly=1, default=lambda self: 'New', string='Employee ID')
    user_id=fields.Many2one("res.users",string="User Id")
    user_name = fields.Char(string='Employee Name', required=True,tracking=True)
    temporary_address=fields.Char(string="Temporary Address")
    permanent_address=fields.Char(string="Permanent Address")
    user_email = fields.Char(string='Email', tracking=True)
    photo=fields.Binary(string="Photo")
    language_spoken=fields.Char(string="Language Spoken")
    age=fields.Integer(string="Age")
    phone=fields.Char(string="Phone",required=True,tracking=True)
    bank_account_number=fields.Char(string="Bank Account Number")
    bank_name=fields.Char(string="Bank Name")
    account_name=fields.Char(string="Account Name")
    bank_phone_number=fields.Char(string="Bank Phone Number")
    job_position = fields.Char()


    # Citizenship Info
    dob = fields.Date(string="DOB",tracking=True)
    nationality=fields.Char(string="Nationality")


    # Family
    father_name = fields.Char(string="Fathers Name")
    mother_name = fields.Char(string="Mothers Name")
    marital_status=fields.Char(string="Marital Status")
    partner_name = fields.Char(string="Partner Name")
    number_of_children=fields.Integer(string="Number of Children")
    grandfather_name = fields.Char(string="GrandFathers Name")
    grandmother_name = fields.Char(string="GrandMothers Name")


    # birth_district=fields.Char(string="Birth District")
    gender=fields.Selection([('male','Male'),('female','Female'),('other','Other')],string="Gender")
    passport_no=fields.Char(string="Passport No.")
    citizenship_no=fields.Char(string="Citizenship No.")
    issued_place=fields.Char(string="Issued Place")
    identification_file=fields.Binary(string="Identification Docs")
    pan = fields.Char(string="PAN No.")
    upload_pan=fields.Binary(string="Pan File")


    # Education Info
    education_ids = fields.One2many('employee.education', 'education_id', string='Education')

    
    # previous work experience
    work_experience_ids = fields.One2many('employee.work.experience', 'request_id', string='Work Experience')

    
    
    # emergency contact
    emergency_contact_id=fields.One2many('employee.emergency.contact','emergency_id',string="Emergency Contact")
    
    
    # work related info
    professional_certifications=fields.Binary(string="Professional Certificate")
    related_skills=fields.Char(string="Skills")
    training_taken=fields.Char(string="Training")
    work_phone=fields.Char(string="Work Phone")
    work_email=fields.Char(string="Work Email")
    position=fields.Char(string="Postion")
    cv = fields.Binary(string="CV")
    department = fields.Char()
    cover_letter=fields.Binary(string="Cover Letter")
    # attachment_ids = fields.Many2many('ir.attachment', string='Attachments')
    training_certificates = fields.Many2many('ir.attachment',string="Training Certificate")
    status=fields.Selection([('pending','Pending'),('accepted','Accepted'),('declined','Declined')],default='pending')
    active = fields.Boolean(default=True)

    @api.model
    def create(self,vals):
        vals['registration_ref']=self.env['ir.sequence'].next_by_code('employee.registration.request.code')
        return super(EmployeeRegistrationRequest,self).create(vals)

    def accept_request(self):
        self.status='accepted'
        template_ref = self.env.ref('employee_dashboard.employee_registration_request_accepted_email_template')
        employee = self.env['hr.employee'].search([('user_id', '=', self.user_id.id)])
        if employee:
            employee.write({
                'employee_ref': self.registration_ref,
                'user_id': self.user_id.id,
                'name': self.user_name,
                'work_email': self.work_email,
                'private_email': self.user_email,
                'image_1920': self.photo,
                'language_spoken': self.language_spoken,
                'age': self.age,
                'temporary_address': self.temporary_address,
                'permanent_address': self.permanent_address,
                'phone': self.phone,
                'bank_account_no': self.bank_account_number,
                'bank_name': self.bank_name,
                'account_name': self.account_name,
                'father_name': self.father_name,
                'mother_name': self.mother_name,
                'marital': self.marital_status,
                'partner_name': self.partner_name,
                'children': self.number_of_children,
                'grandfather_name': self.grandfather_name,
                'birthday': self.dob,
                'nationality': self.nationality,
                'gender': self.gender,
                'passport_id': self.passport_no,
                'identification_id': self.citizenship_no,
                'issued_place': self.issued_place,
                'identification_file': self.identification_file,
                'pan': self.pan,
                'upload_pan': self.upload_pan,
                'professional_certifications': self.professional_certifications,
                'related_skills': self.related_skills,
                'training_taken': self.training_taken,
                'work_phone': self.work_phone,
                'position': self.position,
                'cv': self.cv,
                'cover_letter': self.cover_letter,
                'training_certificates': self.training_certificates,
            })
        else:
            self.env['hr.employee'].create({
                'employee_ref':self.registration_ref,
                'user_id': self.user_id.id,
                'name': self.user_name,
                'work_email': self.work_email,
                'private_email': self.user_email,
                'image_1920': self.photo,
                'language_spoken': self.language_spoken,
                'age': self.age,
                'temporary_address': self.temporary_address,
                'permanent_address': self.permanent_address,
                'phone': self.phone,
                'bank_account_no': self.bank_account_number,
                'bank_name': self.bank_name,
                'account_name': self.account_name,
                'father_name': self.father_name,
                'mother_name': self.mother_name,
                'marital': self.marital_status,
                'partner_name': self.partner_name,
                'children': self.number_of_children,
                'grandfather_name': self.grandfather_name,
                'birthday': self.dob,
                'nationality': self.nationality,
                'gender': self.gender,
                'passport_id': self.passport_no,
                'identification_id': self.citizenship_no,
                'issued_place': self.issued_place,
                'identification_file': self.identification_file,
                'pan': self.pan,
                'upload_pan': self.upload_pan,
                'professional_certifications': self.professional_certifications,
                'related_skills': self.related_skills,
                'training_taken': self.training_taken,
                'work_phone': self.work_phone,
                'position': self.position,
                'cv': self.cv,
                'cover_letter': self.cover_letter,
                'training_certificates': self.training_certificates,
            })
        res_users=self.env['res.users'].search([('id','=',self.user_id.id)])
        if res_users:
            res_users.write({
                'groups_id': [(6, 0, [self.env.ref('employee_dashboard.employee_portal_group').id,self.env.ref('base.group_portal').id])]
            })


        employee_ref = self.env['hr.employee'].search([('user_id', '=', self.user_id.id)])
        for education in self.education_ids:
            education.employee_id = employee_ref.id
        for experience in self.work_experience_ids:
            experience.employee_id = employee_ref.id
        for emergency in self.emergency_contact_id:
            emergency.employee_id = employee_ref.id

        if template_ref:
            template_ref.email_to = self.user_email
            template_ref.body_html = (
                f"<h5>Dear {self.user_name},</h5><hr/><p>You are successfully registered as an employee {self.registration_ref}. Consult with administration for further process </p><hr/><h5>Sangrila Informatics</h5>")
            return template_ref.send_mail(self.id, force_send=True)


    def decline_request(self):
        self.status='declined'
        template_ref = self.env.ref('employee_dashboard.employee_registration_request_rejected_email_template')
        if template_ref:
            template_ref.email_to = self.user_email
            template_ref.body_html = (
                f"<h5>Dear {self.user_name},</h5><hr/><p>Your registration request of an employee has been rejected for now.Please consult with administration for further information </p><hr/><h5>Sangrila Informatics</h5>")
            return template_ref.send_mail(self.id, force_send=True)

    def set_contracts(self):
        return {
            'name': 'Set Contract',
            'type': 'ir.actions.act_window',
            'res_model': 'set.contracts.wizard.model',
            'view_mode': 'form',
            'view_id': self.env.ref('employee_dashboard.view_set_contract_popup').id,
            'target': 'new',
            'context': {
                'default_employee_request_id': self.id
            }
        }

    # def create_employee(self):
    #     pass
    
class EmployeeWorkExperience(models.Model):
    _name = 'employee.work.experience'
    _description = 'Employee Work Experience'

    request_id = fields.Many2one('employee.registration.request', string='Request')
    employee_id=fields.Many2one('hr.employee',string='Employee Id')
    previous_employment = fields.Char(string='Previous Employment')
    job_position = fields.Char(string='Job Position')
    duration_of_employment = fields.Char(string='Duration of Employment')
    company_name = fields.Char(string='Company Name')
    industry = fields.Char(string='Industry')
    responsibilities = fields.Text(string='Responsibilities')
    supervisor_name = fields.Char(string='Supervisor Name')
    supervisor_contact = fields.Char(string='Supervisor Contact')
    exit_reason = fields.Selection([
        ('resignation', 'Resignation'),
        ('termination', 'Termination'),
        ('layoff', 'Layoff'),
        ('retirement', 'Retirement'),
        ('others', 'Others'),
    ], string='Exit Reason')
    exit_comments = fields.Text(string='Exit Comments')
    

class EmployeeEducation(models.Model):
    _name = 'employee.education'
    _description = 'Employee Education'

    CERTIFICATE_LEVEL_SELECTION = [
        ('SEE','SEE'),
        ('+2','+2'),
        ('bachelor', 'Bachelor'),
        ('master', 'Master'),
        ('phd', 'PhD'),
        ('other', 'Other'),
    ]
    education_id = fields.Many2one('employee.registration.request', string='Request')
    employee_id=fields.Many2one('hr.employee',string='Employee Id')
    certificate_level = fields.Selection(selection=CERTIFICATE_LEVEL_SELECTION,string="Certificate Level")
    field_of_study = fields.Char(string="Field Of Study")
    institution_name = fields.Char(string="Institution Name")
    degree_obtained = fields.Char(string="Degree Obtained")
    graduation_year = fields.Date(string="Graduation Year")
    academic_certificates=fields.Many2many('ir.attachment',string="Academic Certificates")
    relevant_courses = fields.Text(string="Relevant Courses")
    notes = fields.Text('Notes..')

class EmergencyContact(models.Model):
    _name = 'employee.emergency.contact'
    _description = 'Employee Emergency Contact'

    emergency_id = fields.Many2one('employee.registration.request', string='Request')
    employee_id=fields.Many2one('hr.employee',string='Employee Id')
    contact_name = fields.Char(string='Contact Name')
    contact_phone = fields.Char(string='Contact Phone')
    relation = fields.Char(string='Relation')


class ContractAndAppointment(models.TransientModel):
    _name = 'set.contracts.wizard.model'
    _description = "Set Contract Transient Model"

    employee_request_id = fields.Many2one('employee.registration.request')
    contract=fields.Binary(string="Contract")

    def save_contract(self):
        request_id=self.employee_request_id
        user_id=request_id.user_id.id
        employee_id=self.env['hr.employee'].search([('user_id','=',user_id)])
        employee_id.write({
            'contract':self.contract
        })


