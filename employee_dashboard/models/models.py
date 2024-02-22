# -*- coding: utf-8 -*-
from odoo import api,models,fields
from odoo.exceptions import ValidationError
from datetime import datetime,date
import base64
from datetime import datetime, timedelta



class LeaveTaken(models.Model):
    _name = 'leave.request'
    _description = "Leave Request"
    _inherit = 'mail.thread'
    _order = 'create_date desc'
    _rec_name = 'employee_id'

    employee_id = fields.Many2one('hr.employee',string="Employee Name")
    department=fields.Char(string="Department")
    start_date=fields.Date(string="Start Date")
    duration_type=fields.Selection([('full-day','Full Day'),('half-day','Half Day')],string="Duration Type",default="full_day")
    date_for_half_leave=fields.Date(string="Leave Date")
    date_for_half_leave_bs=fields.Date(string="Leave Date")
    start_time=fields.Char(string="Start Time")
    end_time=fields.Char(string="End Time")
    start_date_ad = fields.Date()
    end_date_ad = fields.Date()
    ending_date=fields.Date(string='End Date')
    requested_duration=fields.Char(string="Requested Duration")
    allowed_duration=fields.Char(string='Allowed Duration',tracking=True)
    leave_type=fields.Many2one("leave.type",string="Leave Type")
    reason=fields.Char(string="Reason")
    supporting_document= fields.Binary("Supporting Documents",attachment=True)
    status=fields.Selection([('pending','Pending'),('approved','Approved'),('declined','Declined')],tracking=True,string="Status",default='pending')
    _sql_constraints = [
        ('check_dates','CHECK(ending_date >= start_date)','End date must be greater  to start date')
    ]
    
    @api.constrains('start_date_ad')
    def _check_start_date(self):
        for record in self:
            today = fields.Date.today()
            if record.start_date and record.start_date_ad < today:
                raise ValidationError("Start Date cannot be in the past")
            

    # @api.constrains('start_date','ending_date')
    # def check_date_validity(self):
    #     if (self.start_date > self.ending_date):
    #         raise ValidationError("The start date must be earlier than end date")
        


    def get_all_employee(self):
        query = """
            SELECT name from hr_employee where id = 340
        """
        abxd = self._cr.execute(query)
        print(abxd)
        result = self._cr.fetchall()
        for rec in result:
            print(rec[0])
        print(f"Returned using raw db query:::{result}")
        return None
        
    def accept_request(self):  
        self.status = 'approved' 
        print(f"Status is {self.status}")
        template_ref = self.env.ref('employee_dashboard.leave_request_approval_email_template')        
        calendar_event = self.env['office.calender']
        leave_holiday_ref=calendar_event.search([('leave_request_id','=',self.id)])
        if(leave_holiday_ref):
            leave_holiday_ref.write({
                'employee_id': self.employee_id.id,
                'start_date': self.start_date_ad or self.date_for_half_leave,
                'end_date': self.end_date_ad or self.date_for_half_leave,
                'leave_type': self.leave_type.id,
            })
        else:
            calendar_event.create({
                'leave_request_id':self.id,
                'employee_id':self.employee_id.id,
                'start_date':self.start_date_ad or self.date_for_half_leave,
                'end_date':self.end_date_ad or self.date_for_half_leave,
                'leave_type':self.leave_type.id,
            })
        if template_ref:
            template_ref.email_to=self.employee_id.work_email
            if(self.start_date_ad):
                template_ref.body_html=(f"<h5>Dear {self.employee_id.name},</h5><hr/><p>Your leave request has been accepted for {self.allowed_duration} days from {self.start_date_ad} to {self.end_date_ad} date </p><hr/><h5>Sangrila Informatics</h5>")
            elif(self.date_for_half_leave):
                template_ref.body_html=(f"<h5>Dear {self.employee_id.name},</h5><hr/><p>Your leave request has been accepted for day {self.date_for_half_leave} from {self.start_time} to {self.end_time}  </p><hr/><h5>Sangrila Informatics</h5>")
            return template_ref.send_mail(self.id,force_send=True)
        # self.get_all_employee()
        
        return None

        # return{
        #     'type': 'ir.actions.client',
        #     'tag': 'display_notification',
        #     'params': {
        #         'message': 'Request Accepted',
        #         'type': 'success',
        #         'sticky': False,
        #     }
        # }

    def decline_request(self):
        self.status = 'declined'
        template_ref = self.env.ref('employee_dashboard.leave_request_rejected_email_template')        
        if template_ref:
            template_ref.email_to=self.employee_id.work_email
            if(self.start_date_ad):
                template_ref.body_html=(f"<h5>Dear {self.employee_id.name},</h5><hr/><p>Your leave request has been rejected for {self.allowed_duration} days from {self.start_date_ad} to {self.end_date_ad} date </p><hr/><h5>Sangrila Informatics</h5>")
            elif(self.date_for_half_leave):
                template_ref.body_html=(f"<h5>Dear {self.employee_id.name},</h5><hr/><p>Your leave request has been rejected for day {self.date_for_half_leave} from {self.start_time} to {self.end_time}  </p><hr/><h5>Sangrila Informatics</h5>")
            return template_ref.send_mail(self.id,force_send=True)
         
         
      
    def allocate_duration_action(self):
        return {
            'name': 'Enter Counter Duration',
            'type':'ir.actions.act_window',
            'res_model':'allow.duration.wizard.model',
            'view_mode':'form',
            'view_id':self.env.ref('employee_dashboard.view_allowed_duration_popup').id,
            'target':'new',
            'context':{
                'default_leave_request_id':self.id
            }
        }   
        
        


        # return {
        #     'type': 'ir.actions.client',
        #     'tag': 'display_notification',
        #     'params': {
        #         'message': 'Request Denied',
        #         'type': 'danger',
        #         'sticky': False,
        #     }
        # }
class OfficeCalender(models.Model):
    _name = "office.calender"
    _rec_name = "leave_type"
    # other wise we can use compute alsp for _rec_name
    
    leave_type = fields.Many2one('leave.type')
    company_id = fields.Many2one("res.company",string="Company",readonly=True,
                                 default=lambda self:self.env.company)
    holiday_ids = fields.Many2many('office.holidays')
    holiday_date=fields.Date()
    start_date = fields.Date()
    end_date=fields.Date()
    employee_id=fields.Many2one('hr.employee')
    leave_request_id=fields.Many2one('leave.request')
    # related_holiday_name = fields.Char(string="Holiday Name", compute="_compute_related_holiday_name", store=True)

    # @api.depends('holiday_ids.holiday_name')
    # def _compute_related_holiday_name(self):
    #     for record in self: # Adjust as needed
    #         rec_ref = self.env['']
    # @api.depends('holiday_ids.holiday_name')
    # def compute_name(self):
    #     for rec in self:
    #         holiday_names = [holiday.holiday_name for holiday in rec.holiday_ids]

    # @api.depends('holiday_ids.holiday_date')
    # def calculate_holiday_date(self):
    #     for record in self:
    #         # rec = [(6,0,[holiday.holiday_date for holiday in record.holiday_ids])]
    #         date = [holiday.holiday_date for holiday in record.holiday_ids]

    #         print(f"Record for holiday date are {date}")
    #         for dt in date:
    #             record.holiday_date = dt
    #             print(f"Record for holiday date are {dt}")

    # @api.depends('leave_type.holiday_type')
    # def compute_leave_type(self):
    #     for rec in self:
    #         lv_typ = [holiday.holiday_type for holiday in rec.leave_type]
    #         for lv in lv_typ:
    #             print(f"Leave type is {lv}")
    #             rec.leave_type = lv

        
class OfficeHolidays(models.Model):
    _name = "office.holidays" 
    _rec_name = "holiday_name"  
    
    holiday_name = fields.Char(string="Name")
    holiday_date = fields.Date(string="Holiday Date")
    holiday_type = fields.Many2one("leave.type",required=True)
    
    @api.model
    def create(self,vals):
        office_holidays = super(OfficeHolidays,self).create(vals)
        holiday_id = office_holidays.id
        print(f"OFfice holidays id is {holiday_id}")

        #create the office.calender record
        office_calender_vals = {
            "holiday_date": vals.get('holiday_date'),
            "leave_type":vals.get('holiday_type'),
            'holiday_ids':[(4,holiday_id,0)]
        }
        office_calender = self.env['office.calender'].create(office_calender_vals)
        return office_holidays
    
    
    def write(self, vals):
        office_calender_model = self.env['office.calender']
        print(f"Office calender model {office_calender_model}")
        for holiday_record in self:
            office_calender_record = office_calender_model.search([('holiday_ids','=',holiday_record.id)])
            print(f"Office calender rcord :{office_calender_record}")
            if office_calender_record:
                office_calender_record.write({
                    'holiday_date':vals.get('holiday_date'),
                    'leave_type':vals.get('holiday_type')
                })
        res = super(OfficeHolidays, self).write(vals)
        # Your additional logic after writing the record
        return res
    
    def unlnk(self):
        # get the assocated employee records            
        calender_records = self.env['office.calender'].search([('holiday_ids','=',self.ids)])
        # remove the data 
        print(f"ID is {calender_records.id}")
        calender_records.unlink()
        return super(OfficeHolidays, self).unlink()


    
    
    
class LeaveType(models.Model):
    _name = "leave.type" 
    _rec_name = "name"  
    
    name = fields.Char(string="Leave Type")


# this below is the model for the overtime request
class OvertimeRequest(models.Model):
    _name = 'overtime.request'
    _description = "Overtime Request"
    _inherit = 'mail.thread'
    _order = 'create_date desc'


    emp_name = fields.Many2one('hr.employee',string="Employee")
    emp_department = fields.Char("Department")
    emp_involved_project = fields.Char("Involved Project")
    overtime_request_date = fields.Date("Request Date")
    overtime_request_date_in_bs=fields.Date("Request Date(B.S)")
    ot_requested_start_time=fields.Char("Requested Start Time")
    ot_requested_end_time=fields.Char("Requested End Time")
    ot_requested_duration = fields.Char("Requested Duration")
    ot_allowed_duration = fields.Char("Allowed Duration")
    ot_reason = fields.Char("Overtime Reason")
    status=fields.Selection([('pending','Pending'),('approved','Approved'),('declined','Declined')],tracking=True,string="Status",default='pending')


    def accept_request(self):
        self.status = 'approved'
        template_ref = self.env.ref('employee_dashboard.ot_request_approval_email_template')
        if template_ref:
            template_ref.subject = "Approval Of OverTime Request"
            template_ref.email_to = self.emp_name.work_email
            template_ref.body_html = (
                f"<h5>Dear {self.emp_name.name},</h5><hr/><p>Your request for overtime has been accepted for {self.ot_requested_duration} time of day {self.overtime_request_date}</p><hr/><h5>Sangrila Informatics</h5>")
            return template_ref.send_mail(self.id, force_send=True)

    def decline_request(self):
        self.status='declined'
        template_ref = self.env.ref('employee_dashboard.ot_request_rejection_email_template')
        if template_ref:
            template_ref.subject = "Rejection Of OverTime Request"
            template_ref.email_to = self.emp_name.work_email
            template_ref.body_html = (
                f"<h5>Dear {self.emp_name.name},</h5><hr/><p>Your request for overtime has been rejected for {self.ot_requested_duration} time of day {self.overtime_request_date}.Visit administration for more information.</p><hr/><h5>Sangrila Informatics</h5>")
            return template_ref.send_mail(self.id, force_send=True)
    


class ProfileEditRequest(models.Model):
    _name = 'profile.update.request'
    _description = " Profile Update Request"
    _inherit = 'mail.thread'


    employee_name = fields.Many2one("hr.employee",string="Employee_id")
    department=fields.Many2one("hr.department",string="Department")
    phone=fields.Char(string="Phone")
    email=fields.Char(string='Email')
    mobile=fields.Char(string="Mobile")
    street=fields.Char(string="Street")
    city=fields.Char(string="City")
    zip=fields.Char(string="Zip")
    birthdate=fields.Date(string="Birthdate")
    status=fields.Selection([('accepted','Accepted'),('declined','Declined'),('pending','Pending')],string="Status",default="pending")
    marital_status=fields.Selection([('single','Single'),('married','Married'),('cohabitant','Legal Cohabitant'),('widower','Widower'),('divorced','Divorced')],string="Marital Status")
    degree_of_study = fields.Selection(
        [('graduate', 'Graduate'), ('bachelor', 'Bachelor'), ('master', 'Master'), ('doctor', 'Doctor'),
         ('other', 'Other')], string="Degree of Study")
    study_field=fields.Char(string="Study Field")
    study_school=fields.Char(string="Study School")
    bank_detail=fields.Char(string="Bank Detail")
    profile=fields.Image(string="Profile",attachment=True)
    passport_no=fields.Char(string="Passport No.")

    def approve_request(self):
        self.status='accepted'
        employee_ref = self.env['hr.employee'].search([('id', '=', self.employee_name.id)])
        res_partner=self.env['res.partner'].search([('id','=',employee_ref.address_home_id.id)])
        print(res_partner)
        template_ref = self.env.ref('employee_dashboard.profile_update_request_approval_email_template')
        res_partner.street=self.street
        res_partner.city=self.city
        res_partner.zip=self.zip
        res_partner.mobile=self.mobile
        employee_ref.phone=self.phone
        employee_ref.private_email=self.email
        employee_ref.marital=self.marital_status
        employee_ref.certificate=self.degree_of_study
        employee_ref.study_field=self.study_field
        employee_ref.study_school=self.study_school
        # employee_ref.mobile_imei=self.mobile_imei
        # employee_ref.mobile_brand=self.mobile_brand
        if(self.profile):
            employee_ref.image_1920=self.profile
        if template_ref:
            template_ref.subject="Approval Of Profile Update Request"
            template_ref.email_to = self.employee_name.work_email
            template_ref.body_html = (
                    f"<h5>Dear {self.employee_name.name},</h5><hr/><p>Your profile update request has been accepted. You can now view your updated profile.</p><hr/><h5>Sangrila Informatics</h5>")
            return template_ref.send_mail(self.id, force_send=True)

    def decline_request(self):
        self.status='declined'
        print(self.employee_name)
        template_ref = self.env.ref('employee_dashboard.profile_request_rejection_email_template')
        if template_ref:
            template_ref.subject = "Decline Of Profile Update Request"
            template_ref.email_to = self.employee_name.work_email
            template_ref.body_html = (
                f"<h5>Dear {self.employee_name.name},</h5><hr/><p>Your profile update request has been rejected.For more information contact the administration. </p><hr/><h5>Sangrila Informatics</h5>")
            return template_ref.send_mail(self.id, force_send=True)


class AllLogAttendance(models.Model):
    _name = 'all.log.attendance'
    _description = "Logs of all Attendances"

    employee=fields.Many2one('hr.employee',string='Employee')
    # employee_name = fields.Char(string="Employee Name")
    punch_type = fields.Selection([('0', 'Check In'),
                                   ('1', 'Check Out'),
                                   ('2', 'Break Out'),
                                   ('3', 'Break In'),
                                   ('4', 'Overtime In'),
                                   ('5', 'Overtime Out')], string='Punching Type')
    punching_time = fields.Datetime(string='Punching Time')
    punching_latitude=fields.Float(string='Punching Latitude',digits=(10,7))
    punching_longitude=fields.Float(string='Punching Longitude',digits=(10,7))
    punching_address=fields.Char(string='Punching Address',digits=(10,7))
    proof=fields.Binary(string="Proof Document")

    @api.model
    def create(self, vals_list):
        result=super(AllLogAttendance, self).create(vals_list)
        self._update_attendance(vals_list)
        return result

    def _update_attendance(self, vals):
        employee = vals['employee']
        punch_type = vals['punch_type']
        punching_time = vals['punching_time']
        punching_latitude = vals['punching_latitude']
        punching_longitude = vals['punching_longitude']
        punching_address = vals['punching_address']
        attendance = self.env['hr.attendance']
        proof = vals['proof']
        date_time_object_utc = fields.Datetime.from_string(punching_time)
        date_only = date_time_object_utc.date()
        print(date_only)
        date_obtained_start = fields.Datetime.to_string(
            fields.Datetime.from_string(str(date_only)))  # Convert date to datetime
        date_obtained_end = fields.Datetime.to_string(
            fields.Datetime.from_string(str(date_only)) + timedelta(days=1))  # Next day
        previous_attendance = attendance.search(
            [('employee_id', '=', employee), ('check_in', '>=', date_obtained_start),
             ('check_in', '<', date_obtained_end)])
        if previous_attendance:
            if punch_type == '1':
                previous_attendance.write({
                    'check_out': punching_time,
                    'checkout_latitude': punching_latitude,
                    'checkout_longitude': punching_longitude,
                    'checkout_location': punching_address,
                    'proof_checkout': proof
                })
        else:
            if punch_type == '0':
                previous_day_attendance = attendance.search([('employee_id', '=', employee)], order='write_date desc',
                                                            limit=1)
                previous_day_checkout = previous_day_attendance.check_out
                print(previous_day_checkout)
                if (previous_day_checkout == False):
                    previous_day_attendance.write({
                        'active': False,
                    })

                attendance.create({
                    'employee_id': employee,
                    'check_in': punching_time,
                    'checkin_latitude': punching_latitude,
                    'checkin_longitude': punching_longitude,
                    'checkin_location': punching_address,
                    'proof_checkin': proof
                })

        pass


class AllowDurationPopup(models.TransientModel):
    _name = 'allow.duration.wizard.model'
    _description = "Allow Duration Transient Model"


    leave_request_id =  fields.Many2one('leave.request')
    duration_count = fields.Char('Allocate Duration')
    leave_start_date = fields.Date("Leave Start Date")
    leave_end_date = fields.Date("Leave End Date")

        
    
    def update_counter_offer_price(self):
        date_gap = self.leave_end_date - self.leave_start_date
        print(date_gap)
        gap_in_days = date_gap.days
        gap_in_string = f"{date_gap.days+1} days"
        self.env['leave.request'].search([('id','=',self.leave_request_id.id)]).write({
            'allowed_duration':gap_in_string,
            'start_date_ad':self.leave_start_date,
            'end_date_ad':self.leave_end_date
        })
    
    
    #  context="{'search_default_employee_id': id, 'search_default_check_in_filter': '1'}" 