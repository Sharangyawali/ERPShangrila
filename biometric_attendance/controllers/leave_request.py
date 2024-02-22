from odoo import http
from odoo.http import request

class RequestForLeave(http.Controller):

    @http.route('/leave_request',auth='public',type='http', website=True,cors='*')
    def render_leave_request_page(self):
        partner = request.env.user.name
        print("Hello")
        department=request.env['hr.employee'].search([('name','=',partner)])
        department_id=department.department_id
        required_department=department_id.name
        print(required_department)
        # leave_type_ref=request.env['leave.type'].sudo().search([])
        leave_list=[]
        leave_type_ref = [1,2,3,4,5,6,6]
        for rec in leave_type_ref:
            leave_list.append(
                {
                    'leave_type':"wjwjjwjw"
                    }
                    )
        # employee_list_ref = request.env['hr.employee'].sudo().search([])
        # # print(vehicle_list)
        # employee_list = []
        # for rec in employee_list_ref:
        #     employee_name= rec.name
        #     employee_list.append(employee_name)


        return request.render('biometric_attendance.leave_request',{'department':required_department,'leave_type':leave_list})

    @http.route('/submit/leave_request', auth='public', type='http', methods=['POST'], csrf=False, website=True)
    def submit_leave_request(self, **post):
        employeeName = post.get('employeeName')
        department=post.get('department')
        leave_type=post.get('leave_type')
        start_date=post.get('startDate')
        ending_date=post.get('endingDate')
        requested_duration=post.get('requested_duration')
        reason=post.get('reason')

        leave_request_model_ref = http.request.env['leave.permission'].create({
            'employee_name':employeeName,
            'department':department,
            'start_date':start_date,
            'ending_date': ending_date,
            'requested_duration': requested_duration,
            'leave_type': leave_type,
            'reason':reason,
        })

        print(leave_request_model_ref)

        return request.redirect('/')