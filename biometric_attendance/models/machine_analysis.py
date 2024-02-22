# -*- coding: utf-8 -*-
###################################################################################
#
#    Cybrosys Technologies Pvt. Ltd.
#    Copyright (C) 2022-TODAY Cybrosys Technologies(<http://www.cybrosys.com>).
#    Author: cybrosys(<https://www.cybrosys.com>)
#
#    This program is free software: you can modify
#    it under the terms of the GNU Affero General Public License (AGPL) as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###################################################################################
from odoo import tools
from odoo import models, fields, api, _


class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    device_id = fields.Char(string='Biometric Device ID')
    # portal_user_id = fields.Many
    



class ZkMachine(models.Model):
    _name = 'zk.machine.attendance'
    _inherit = 'hr.attendance'

    @api.constrains('check_in', 'check_out', 'employee_id')
    def _check_validity(self):
        """overriding the __check_validity function for employee attendance."""
        pass

    device_id = fields.Char(string='Biometric Device ID')
    punch_type = fields.Selection([('0', 'Check In'),
                                   ('1', 'Check Out'),
                                   ('2', 'Break Out'),
                                   ('3', 'Break In'),
                                   ('4', 'Overtime In'),
                                   ('5', 'Overtime Out')],
                                  string='Punching Type')

    attendance_type = fields.Selection([('1', 'Finger'),
                                        ('15', 'Face'),
                                        ('2','Type_2'),
                                        ('3','Password'),
                                        ('4','Card')], string='Category')
    punching_time = fields.Datetime(string='Punching Time')
    address_id = fields.Many2one('res.partner', string='Working Address')



class ReportZkDevice(models.Model):
    _name = 'zk.report.daily.attendance'
    _auto = False
    # _order = 'data_date desc'

    name = fields.Many2one('hr.employee', string='Employee')
    punching_day = fields.Datetime(string='Date')
    address_id = fields.Many2one('res.partner', string='Working Address')
    attendance_type = fields.Selection([('1', 'Finger'),
                                        ('15', 'Face'),
                                        ('2','Type_2'),
                                        ('3','Password'),
                                        ('4','Card')],
                                       string='Category')
    punch_type = fields.Selection([('0', 'Check In'),
                                   ('1', 'Check Out'),
                                   ('2', 'Break Out'),
                                   ('3', 'Break In'),
                                   ('4', 'Overtime In'),
                                   ('5', 'Overtime Out')], string='Punching Type')
    punching_time = fields.Datetime(string='Punching Time')
    data_date = fields.Date("Record Date",compute='_compute_data_date')

    @api.depends('punching_time')
    def _compute_data_date(self):
        for record in self:
            if record.punching_time:
                record.data_date = record.punching_time.date()


    def update_checkin_checkout(self):
        # Retrieve all unique employees
        employees = self.env['zk.report.daily.attendance'].sudo().search([]).mapped('name')
        # print(employees)
        hr_att_ref = self.env['hr.attendance']
        # print(hr_att_ref)

        for employee in employees:

            # print(f"This is for employee: {employee.name}")
            # Retrieve all records for the employee
            dates = self.env['zk.report.daily.attendance'].sudo().search([
                ('name', '=', employee.id),
            ]).mapped('data_date')
            
            # Convert the list of dates to a set to remove duplicates
            unique_dates = set(dates)


            if unique_dates:
                for date in unique_dates:
                    # print(record)
                    print(f"\nRecords for {employee.name} on {date}:")
                    # print(date)
                    records_for_employee = self.env['zk.report.daily.attendance'].sudo().search([
                        ('name', '=', employee.id),
                    ])
                    # filter the records based on the date
                    records_for_date = [record for record in records_for_employee if record.data_date == date]

                    if records_for_date:
                        # for record in records_for_date:
                        #     # print(record)
                        #     # print(
                        #     #     f"ID: {record.name}, Punching Time: {record.punching_time}"
                        #     # )

                            # # Find the earliest and latest punching times for the specific date
                        check_in = min(records_for_date, key=lambda r: r.punching_time).punching_time
                        check_out = max(records_for_date, key=lambda r: r.punching_time).punching_time
                        if check_in or  check_out:
                            duplicate_check = self.env['hr.attendance'].search([
                                ('employee_id','=',employee.id),
                                ('check_in','=',check_in),
                                ('check_out','=',check_out),
                            ])
                            if duplicate_check:
                                print("Duplicate found")
                                continue
                            else:
                                hr_att_ref.create({
                                    'employee_id': employee.id,
                                    'check_in': check_in,
                                    'check_out': check_out
                            })
                                print(
                                    f" Check in: {check_in},check out:{check_out}"
                                )
                        else:
                            hr_att_ref.create({
                                'employee_id': employee.id,
                                'check_in': False,
                                'check_out': False
                           })

                            # # Now you can use check_in and check_out as needed

                    else:
                        pass
     
    def init(self):
        tools.drop_view_if_exists(self._cr, 'zk_report_daily_attendance')
        query = """
            create or replace view zk_report_daily_attendance as (
                select
                    min(z.id) as id,
                    z.employee_id as name,
                    z.write_date as punching_day,
                    z.address_id as address_id,
                    z.attendance_type as attendance_type,
                    z.punching_time as punching_time,
                    z.punch_type as punch_type
                from zk_machine_attendance z
                    join hr_employee e on (z.employee_id=e.id)
                GROUP BY
                    z.employee_id,
                    z.write_date,
                    z.address_id,
                    z.attendance_type,
                    z.punch_type,
                    z.punching_time
            )
        """
        self._cr.execute(query)
        
    


