# -*- coding: utf-8 -*-
from odoo import api, models, fields


class EmployeeInherit(models.Model):
    _inherit = 'hr.employee'

    leave_request_count = fields.Integer(
        string="Leave Count", compute="_compute_employee_leave_count")
    address_home_id = fields.Many2one(
        'res.partner',
        'Address',
        help='Enter here the private address of the employee, not the one linked to your company.',
        groups="hr.group_hr_user,employee_dashboard.employee_portal_group",
        tracking=True,
        domain="['|', ('company_id', '=', False), ('company_id', '=', company_id)]"
    )
    @api.depends('user_id')
    def _compute_employee_leave_count(self):
        # print(f"Employee -s {employee}")
        if self.id:
                print(self.id)
                leave_count = self.env['leave.request'].search_count([
                    ('employee_id', '=', self.id)
                ])
                print(f"Leave count for {self.name}: {leave_count}")
                if leave_count:
                    self.leave_request_count = leave_count
                else:
                   self.leave_request_count = 0
        else:
            # print(f"Employee:{self.name} is passed with user_id having {self.user_id}")
            self.leave_request_count = 0
            

    def get_all_employee(self):
        query = """
            SELECT id from hr_employee
        """
        self._cr_execute(query)
        result = self._cr.fetchall(query)
        print(f"Returned using raw db query:::{result}")
        # leave_data = self.env['leave.request'].sudo()._read_group([
        #     ('employee_name', '=', employee.user_id.name)], ['status'], ['status'])

        # # Assuming leave_data is a list of dictionaries
        # if leave_data:
        #     # Assuming you are interested in the first record
        #     first_record = leave_data[0]
        #     print(leave_data)
        #     employee.leave_request_count = first_record.get(
        #         'status', {}).get('count', 0)
        # else:
        #     employee.leave_request_count = 0
