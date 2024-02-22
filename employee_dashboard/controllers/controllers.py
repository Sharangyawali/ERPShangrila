# -*- coding: utf-8 -*-
from odoo import http,fields
from odoo.http import request
from datetime import datetime,timedelta
from dateutil.relativedelta import relativedelta
import base64
from werkzeug.http import parse_accept_header
from ua_parser import user_agent_parser
from odoo.exceptions import ValidationError
import json



class EmployeeDashboard(http.Controller):
    @http.route('/leaveRequest', auth='user', website=True)
    def index(self, **kw):
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group('employee_dashboard.employee_internal_user_group')
        dept_details=False
        if (is_in_group):
            dept_details=True
        department = request.env['hr.employee'].search(
            [('user_id', '=', request.env.user.id)])
        show=False
        if(department):
            show=True
        department_name = department.department_id.name
        leave_type=request.env['leave.type'].sudo().search([])
        print(leave_type)
        leave_list=[]
        for ll in leave_type:
            leave_list.append({'id':ll.id,'name':ll.name})
        print(leave_list)
        return request.render("employee_dashboard.leave_request_page", {'department': department_name,'show':show,'leave_type':leave_list,'dept':dept_details})

    @http.route('/submit/leaveRequest',methods=['POST'], csrf=False,auth='user',website=True)
    def submit_leave_request(self, **post):
        employee_ref = request.env['hr.employee'].search([('user_id','=',request.env.user.id)])
        print(f"Department ID is {employee_ref.department_id}")
        leave_type=post.get('leave-type')
        duration_type=post.get('duration_type')
        print(duration_type)
        
        # Date in ad
        if(duration_type=='full-day'):
            start_date_ad = post.get('start-date')
            end_date_ad = post.get('end-date')

            # Get the datetime in sring format in YY-MM-DD
            start_date_bs_str=post.get('start-date-bs')
            ending_date_bs_str=post.get('end-date-bs')
            start_date_bs = datetime.strptime(start_date_bs_str,'%Y-%m-%d')
            end_date_bs = datetime.strptime(ending_date_bs_str,'%Y-%m-%d')
            date_gap = end_date_bs - start_date_bs
            gap_in_days = date_gap.days
            gap_in_string = f"{gap_in_days+1} days"
            # if gap_in_days == 0:
            #     gap_in_string = "1 day"
            date_for_half_leave_bs=False
            date_for_half_leave=False
            start_time=False
            end_time=False
        else:
            start_date_bs=False
            end_date_bs=False
            start_date_ad=False
            end_date_ad=False
            gap_in_string=False
            date_for_half_leave_bs_str=post.get('date_for_half_leave_bs')
            date_for_half_leave=post.get('date_for_half_leave')
            date_for_half_leave_bs=datetime.strptime(date_for_half_leave_bs_str,'%Y-%m-%d')
            start_time=post.get('start_time')
            end_time=post.get('end_time')
        reason=post.get('reason')
        department_name = employee_ref.department_id.name if employee_ref.department_id else 'Not Found'
        proof_document = request.httprequest.files.get('proofForLeave')
        if proof_document:
            file_data = proof_document.read()
            file_name = proof_document.filename
            file_data_base64 = base64.b64encode(file_data)
        else:
            file_data_base64=False
        leave_request_model_ref = http.request.env['leave.request'].sudo().create({
            'employee_id':employee_ref.id,
            'department':department_name,
            'start_date':start_date_bs,
            'ending_date': end_date_bs,
            'start_date_ad':start_date_ad,
            'end_date_ad':end_date_ad,
            'date_for_half_leave_bs':date_for_half_leave_bs,
            'date_for_half_leave':date_for_half_leave,
            'start_time':start_time,
            'end_time':end_time,
            'requested_duration': gap_in_string,
            'leave_type': leave_type,
            'duration_type':duration_type,
            'reason':reason,
            'supporting_document':file_data_base64,
        })
        return request.redirect('/')
    
    @http.route('/attendance_history', auth='user', website=True)
    def attendance_history(self,page=1, **kw):
        page = int(page)
        row_per_page = 10
        offset = (page - 1) * row_per_page
        limit = page * row_per_page
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group('employee_dashboard.employee_internal_user_group')
        dept_details = False
        if (is_in_group):
            dept_details = True
        current_user = request.env.user.id

        employee_ref = request.env['hr.employee'].search([
            ('user_id', '=', current_user)
        ])
        show=False
        if(employee_ref):
            show=True
        # print(employee_ref.name)
        attendance_data = request.env['hr.attendance'].search([
            ('employee_id', '=', employee_ref.id)
        ])
        attendance_list = []
        i = 1
        for attendance in attendance_data:
            worked_hours_formatted = round(attendance.worked_hours, 2)
            attendance_list.append({
                'id': i,
                'record_date': attendance.check_in.date(),
                'check_in': attendance.check_in,
                'check_out': attendance.check_out,
                'worked_hours': worked_hours_formatted
            })
            i = i+1
        print("Current User:{}".format(current_user))
        print(attendance_list)
        attendance_list2=attendance_list[offset:limit]
        page_count=int(len(attendance_list)/row_per_page)
        return request.render("employee_dashboard.attendance_history_page", {"attendances": attendance_list2,'show':show,'dept':dept_details,'page_count':page_count})

    @http.route('/checkin_checkout_page', auth='public',website=True)
    def attendance_page(self, **kw):
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group('employee_dashboard.employee_internal_user_group')
        dept_details = False
        if (is_in_group):
            dept_details = True
        employee_ref = request.env['hr.employee'].search(
            [('user_id', '=', request.env.user.id)])
        show = False
        if (employee_ref):
            show = True
        # is_touch_device = platform.touchscreen()
        # print(is_touch_device)
        # mobile_operating_systems = ["Android", "Darwin", "Windows"]  # Add more as needed
        # print(platform.system())
        # is_mobile_os = platform.system() in mobile_operating_systems
        # print(is_mobile_os)
        user_agent_string = http.request.httprequest.headers.get('User-Agent', '')
        print(user_agent_string)
        print(parse_accept_header(user_agent_string))
        is_mobile = 'mobile' in parse_accept_header(user_agent_string) or 'iPhone' in parse_accept_header(user_agent_string) or 'Android' in parse_accept_header(user_agent_string) or 'Redmi' in parse_accept_header(user_agent_string)
        user_agent_info = user_agent_parser.Parse(user_agent_string)
        print(user_agent_info)
        # is_mobile2=((user_agent_info['device']['family']=='iPhone') and (user_agent_info['os']['patch'] is not None) or ((user_agent_info['device']['family']=='K') and (user_agent_info['user_agent']['patch'] is not None) ))
        # is_mobile2=((user_agent_info['device']['family']=='iPhone') or ((user_agent_info['device']['family']=='K') and (user_agent_info['user_agent']['patch'] is not None) ))
        # is_mobile=True
        # if os.environ.get('DEBUG_MODE') == 'True':  # Server-side check
        #     return render_template('debug_view.html')
        # elif request.args.get('debug'):  # Check for request parameter
        #     return render_template('debug_view.html')
        # else:
        #     return render_template('normal_view.html')
        print(is_mobile)
        # print(is_mobile2)
        # if is_mobile and  is_mobile2:
        # is_mobile=True
        if is_mobile:
            current_user = request.env.user.id
            user_id=request.env['hr.employee'].search([('user_id','=',current_user)])
            return request.render("employee_dashboard.checkin_checkout_page",{'id':user_id,'display':True,'show':show,'dept':dept_details})
        else:
            return request.render("employee_dashboard.checkin_checkout_in_desktop",{'show':show,'dept':dept_details})

    # this is for the dashboard
    @http.route('/', auth='user',website=True)
    def dashboard_page(self, **kw):
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group('employee_dashboard.employee_internal_user_group')
        dept_details = False
        if (is_in_group):
            dept_details = True
        current_user=request.env['hr.employee'].search([('user_id','=',request.env.user.id)])
        show=False
        if current_user:
            show=True
        attendance=request.env['hr.attendance'].search([('employee_id','=',current_user.id),('active','=',True)])
        archived=request.env['hr.attendance'].search([('employee_id','=',current_user.id),('active','=',False)])
        total_present_days=len(attendance)
        leave_request=request.env['leave.request'].search([('employee_id','=',current_user.id),('status','=','approved')])
        print(total_present_days)
        leave_count=len(leave_request)
        worked_hours=0
        archived_in_last_30_days=0
        present_days_in_last_30_days=0
        worked_hours_in_last_30_days=0
        archived_attendance=len(archived)
        today=datetime.now().date()
        date_before_30_days=today-timedelta(days=30)
        print(date_before_30_days)
        for att in attendance:
            worked_hours=worked_hours+att.worked_hours
            print(att.check_in.date())
            if att.check_in.date()>=date_before_30_days:
                present_days_in_last_30_days=present_days_in_last_30_days+1
                worked_hours_in_last_30_days=worked_hours_in_last_30_days+att.worked_hours
        for ar in archived:
            if ar.create_date.date()>=date_before_30_days:
                archived_in_last_30_days=archived_in_last_30_days+1
        monthly_attendance = {}
        for month in range(1, 13):
            first_day_of_month = datetime(today.year, month, 1, 0, 0, 0)

            attendance = request.env['hr.attendance'].search([
                ('employee_id', '=', current_user.id),
                ('active', '=', True),
                ('check_in', '>=', fields.Datetime.to_string(first_day_of_month)),
                ('check_in', '<', fields.Datetime.to_string(first_day_of_month + relativedelta(months=1))),
            ])

            monthly_attendance[month] = len(attendance)
        print(monthly_attendance)
        return request.render("employee_dashboard.dashboard_page",
                              {'total_present_days':total_present_days,
                               'worked_hours':round(worked_hours,2),
                               'leave_count':leave_count,
                               'present_days_in_last_30_days':present_days_in_last_30_days,
                               'archived_attendance':archived_in_last_30_days,
                               'worked_hours_in_last_30_days':worked_hours_in_last_30_days,
                               'monthly_attendance':monthly_attendance,
                               'show':show,
                               'dept':dept_details,})

    @http.route('/leave_history_page', auth='user', website=True)
    def leave_history_page(self,page=1, **kw):
        page = int(page)
        row_per_page = 10
        offset = (page - 1) * row_per_page
        limit = page * row_per_page
        print(page)
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group('employee_dashboard.employee_internal_user_group')
        dept_details = False
        if (is_in_group):
            dept_details = True
        current_user = request.env.user.id
        employee_ref = request.env['hr.employee'].search(
            [('user_id', '=', current_user)])
        show=False
        if(employee_ref):
            show=True
        print(f"Current Employee is ::{employee_ref} ")
        print(employee_ref.id)
        leave_ref = request.env['leave.request'].search(
            [('employee_id', '=', employee_ref.id)])
        print(leave_ref)
        leave_list = []

        i = 1
        for leave_data in leave_ref:
            leave_list.append({
                's_no': i,
                'request_date': leave_data.create_date.date(),
                'leave_type': leave_data.leave_type.name,
                'reason': leave_data.reason,
                'status': leave_data.status,
                'start_date': leave_data.start_date or leave_data.date_for_half_leave,
                'end_date': leave_data.ending_date or leave_data.date_for_half_leave,
                'allowed_duration': leave_data.allowed_duration
            })
            i = i+1
        leave_list2=leave_list[offset:limit]
        page_count=int(len(leave_list)/row_per_page)
        return request.render("employee_dashboard.leave_history_page", {'leave_list': leave_list2,'show':show,'dept':dept_details,'page_count':page_count})

    @http.route('/view_profile', auth='public', website=True)
    def user_profile_page(self, **kw):
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group('employee_dashboard.employee_internal_user_group')
        dept_details = False
        if (is_in_group):
            dept_details = True
        current_user = request.env.user.id
        print(current_user)
        employee_ref = request.env['hr.employee'].sudo().search([
            ('user_id', '=', current_user)
        ])
        show=False
        if(employee_ref):
            show=True
        print(employee_ref)
        department_list = []
        departments = request.env['hr.department'].sudo().search([])
        # profile_image_base64 = base64.b64encode(employee_ref.image_1920).decode('utf-8')
        for dr in departments:
            department_list.append({'id': dr.id, 'name': dr.name})
        print(department_list)
        return request.render("employee_dashboard.view_profile_page", {'employee': employee_ref, 'department': department_list,'show':show,'dept':dept_details})

    @http.route('/submit/edit_profile', methods=['POST'], csrf=False, auth='user', website=True)
    def submit_edit_profile(self, **post):
        employee = post.get('employee_name')
        employee_ref = request.env['hr.employee'].sudo().search(
            [('name', '=', employee)])
        employee_name = employee_ref.id
        department_name = post.get('department')
        department_ref = request.env['hr.department'].sudo().search(
            [('name', '=', department_name)])
        department = department_ref.id
        phone = post.get('phone')
        email = post.get('email')
        mobile = post.get('mobile')
        street = post.get('street')
        city = post.get('city')
        birthdate = post.get('birthdate') or False
        zip = post.get('zip')
        marital_status = post.get('marital_status')
        degree_of_study = post.get('degree_of_study')
        study_field = post.get('study_field')
        study_school = post.get('study_school')
        bank_detail = post.get('bank_detail')
        passport_no = post.get('passport_no')
        proof_document = request.httprequest.files.get('editImageInput')
        file_data = proof_document.read()
        file_name = proof_document.filename
        profile = base64.b64encode(file_data)
        http.request.env['profile.update.request'].create({
            'employee_name': employee_name,
            'department': department,
            'phone': phone,
            'email': email,
            'mobile': mobile,
            'street': street,
            'city': city,
            'birthdate': birthdate,
            'zip': zip,
            'marital_status': marital_status,
            'degree_of_study': degree_of_study,
            'study_field': study_field,
            'study_school': study_school,
            'bank_detail': bank_detail,
            'passport_no': passport_no,
            'profile': profile,
        })
        return request.redirect('/')
        # this below is for the calender page in the employee dashboard

    @http.route('/yearly_calender', auth='user', website=True)
    def calendar_page(self, **kw):
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group('employee_dashboard.employee_internal_user_group')
        dept_details = False
        if (is_in_group):
            dept_details = True
        employee_ref = request.env['hr.employee'].search(
            [('user_id', '=', request.env.user.id)])
        show = False
        if (employee_ref):
            show = True
        return request.render("employee_dashboard.yearly_calender_page", {'show':show,'dept':dept_details})



    @http.route('/ot_request_form', auth='user', website=True)
    def ot_request_form(self, **kw):
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group('employee_dashboard.employee_internal_user_group')
        dept_details = False
        if (is_in_group):
            dept_details = True
        emp_ref = request.env['hr.employee'].search(
            [('user_id', '=', request.env.user.id)])
        show=False
        if(emp_ref):
            show=True
        department_name = emp_ref.department_id.name if emp_ref.department_id else 'Not Found'
        print(department_name)
        return http.request.render('employee_dashboard.overtime_request_page', {'department': department_name,'show':show,'dept':dept_details})

    @http.route('/submit/ot_request_form', auth='user', methods=['POST'], website=True, csrf=False)
    def submit_ot_request_form(self, **kw):
        user = request.env.user.id
        employee_ref = request.env['hr.employee'].search(
            [('user_id', '=', request.env.user.id)])
        emp_involved_project = kw.get('project_involved')
        request_date = kw.get('date')
        request_Date_in_bs=kw.get('date_in_bs')
        ot_requested_start_time = kw.get('start_time')
        ot_requested_end_time = kw.get('time')
        print(ot_requested_start_time,ot_requested_end_time)
        time1 = datetime.strptime(ot_requested_start_time, '%H:%M')
        time2 = datetime.strptime(ot_requested_end_time, '%H:%M')
        ot_requested_duration=time2-time1
        print(ot_requested_duration)
        reason_for_overtime = kw.get('reason')
        department_name = employee_ref.department_id.name if employee_ref.department_id else 'Not Found'
        request.env['overtime.request'].create({
            'emp_name': employee_ref.id,
            'emp_department': department_name,
            'emp_involved_project': emp_involved_project,
            'overtime_request_date': request_date,
            'overtime_request_date_in_bs': request_Date_in_bs,
            'ot_requested_start_time':ot_requested_start_time,
            'ot_requested_end_time': ot_requested_end_time,
            'ot_requested_duration':ot_requested_duration,
            'ot_reason': reason_for_overtime
        })
        return request.redirect('/')

    @http.route('/ot_history_page', auth='public', website=True)
    def ot_history_page(self,page=1, **kw):
        page = int(page)
        row_per_page = 10
        offset = (page - 1) * row_per_page
        limit = page * row_per_page
        print(page)
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group('employee_dashboard.employee_internal_user_group')
        dept_details = False
        if (is_in_group):
            dept_details = True
        employee_ref = request.env['hr.employee'].search(
            [('user_id', '=', request.env.user.id)])
        show=False
        if(employee_ref):
            show=True
        ot_ref = request.env['overtime.request'].search([('emp_name','=',employee_ref.id)])
        print(ot_ref)
        ot_list = []
        i = 1
        for ot_data in ot_ref:
            ot_list.append({
                's_no': i,
                # 'request_date': ot_data.create_date.date(),
                'emp_department': ot_data.emp_department,
                'emp_involved_project': ot_data.emp_involved_project,
                # Corrected variable name here
                'overtime_request_date': ot_data.overtime_request_date,
                # Corrected variable name here
                'ot_requested_duration': ot_data.ot_requested_duration,
                'ot_reason': ot_data.ot_reason,
                'status': ot_data.status,
            })
            i += 1
        ot_list2=ot_list[offset:limit]
        page_count=int(len(ot_list)/row_per_page)
        return request.render("employee_dashboard.overtime_history_page", {'ot_list': ot_list2,'show':show,'dept':dept_details,'page_count':page_count})

    @http.route('/departments_attendances', auth='user', website=True)
    def departments_details(self, **kw):
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group('employee_dashboard.employee_internal_user_group')
        if(is_in_group):
            employee_ref = request.env['hr.employee'].search(
                [('user_id', '=', request.env.user.id)])
            show = False
            if (employee_ref):
                show = True
            department=request.env['hr.department'].search([('id','=',employee_ref.department_id.id)])
            employees=department.member_ids
            attendance_list=[]
            attendance_list2=[]
            i=1
            for em in employees:
                attendance=request.env['hr.attendance'].search([('employee_id','=',em.id)])
                for att in attendance:
                    if(employee_ref.id is not att.employee_id.id):
                        attendance_list.append({
                            'id':i,
                            'name':em.name,
                            'check_in':att.check_in,
                            'check_out':att.check_out,
                            'checkin_add':att.checkin_location,
                            'checkout_add':att.checkout_location,
                            'worked_hour':round(att.worked_hours,2)
                        })
                        attendance_list2.append({
                            'id': i,
                            'name': em.name,
                            'check_in': self.serialize_datetime(att.check_in),
                            'check_out': self.serialize_datetime(att.check_out),
                            'checkin_add': att.checkin_location,
                            'checkout_add': att.checkout_location,
                            'worked_hour': round(att.worked_hours, 2)
                        })
                        i=i+1
            attendance_json = json.dumps(attendance_list2)

            return request.render("employee_dashboard.department_details_page", {'show':show,'attendance':attendance_list,'attendance_json':attendance_json,'dept':True})

    def serialize_datetime(self, dt):
        if isinstance(dt, datetime):
            return dt.isoformat()
        return None

    @http.route('/department_leave', auth='public', website=True)
    def department_leave(self,page=1, **kw):
        page=int(page)
        row_per_page=10
        offset=(page-1)*row_per_page
        limit=page*row_per_page
        print(page)
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group('employee_dashboard.employee_internal_user_group')
        dept_details = False
        if (is_in_group):
            dept_details = True

        current_user = request.env.user.id
        employee_ref = request.env['hr.employee'].search([('user_id', '=', current_user)])
        show = False
        if (employee_ref):
            show = True
        leave_list_of_collegues = []
        j = 1
        employee_in_department_ref = request.env['hr.employee'].search(
            [('department_id', '=', employee_ref.department_id.id)])
        for emp in employee_in_department_ref:
            if (emp.id is not employee_ref.id):
                leave_request = request.env['leave.request'].search(
                    [('employee_id', '=', emp.id), ('status', '=', 'approved')])
                for lr in leave_request:
                    todays_date = fields.Date.today()
                    if ((lr.duration_type == 'full-day') and ((lr.start_date_ad >= todays_date) or (
                            lr.start_date_ad < todays_date and lr.end_date_ad >= todays_date))) or (
                            (lr.duration_type == 'half-day') and (lr.date_for_half_leave >= todays_date)):
                        leave_list_of_collegues.append({
                            's_no': j,
                            'Name': emp.name,
                            'duration_type': lr.duration_type,
                            'leave_type': lr.leave_type.name,
                            'start_date': lr.start_date or lr.date_for_half_leave_bs,
                            'end_date': lr.ending_date,
                            'allowed_duration': lr.allowed_duration
                        })
                        j=j+1
        leave_list=leave_list_of_collegues[offset:limit]
        page_count=int(len(leave_list_of_collegues)/row_per_page)
        print(page_count)
        return request.render("employee_dashboard.department_in_leave", {'leave_list':leave_list,'show':show,'dept':dept_details,'page_count':page_count})

    @http.route('/kitchen_requests',auth='user',cors='*', website=True)
    def kitchen_request(self,day_of_week='sunday',**kw):
        user = request.env.user
        is_in_group = user.has_group('employee_dashboard.employee_admin_group') or user.has_group('employee_dashboard.employee_internal_user_group')
        dept_details = False
        if (is_in_group):
            dept_details = True
        current_user=request.env.user.id
        employee_ref = request.env['hr.employee'].search([('user_id', '=', current_user)])
        show = False
        if (employee_ref):
            show = True

        foods=request.env['food.mapping'].sudo().search([])
        day=day_of_week
        return request.render("employee_dashboard.kitchen_request_template", {'show':show,'dept':dept_details,'foods':foods,'day':day,'i':0,})

    @http.route('/submit/kitchen_requests',methods=['POST'],csrf=False,auth='user', website=True)
    def kitchen_request_submit(self,**post):
        user=request.env.user.id
        employee_ref=request.env['hr.employee'].search([('user_id','=',user)])
        day_of_week=post.get('days_of_week')
        meal_time=request.httprequest.form.getlist('meal_time')
        checked = []
        food_list=[]
        for i in range(len(meal_time)):
            check_key = f'flexCheckDefault_{i}'
            check_value = post.get(check_key)

            if check_value is None:
                check_value="Not Attending"

            checked.append(check_value)
            j=0
            meal_inside=[]
            while True:
                meal_key = f'meal_name_{i}_{j}'
                meal_name = post.get(meal_key)
                if meal_name is None:
                    break  # Break the loop if no more meal times are found for the current 'i'
                meal_inside.append(meal_name)

                j += 1
            food_list.append(meal_inside)
        print(food_list)
        for k in range(len(meal_time)):
            made=request.env['meal.request'].sudo().create({
                'employee_id':employee_ref.id,
                'meal_time':meal_time[k],
                'day_of_week':day_of_week,
                'state':checked[k]
            })
            food_to_append=[]
            food_to_append.append((6, 0, food_list[k]))
            made.sudo().write({
                'food_id':food_to_append
            })

        return request.redirect('/')
