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
import pytz
import sys
import datetime
import logging
import binascii
from datetime import datetime, timedelta

from . import zklib
from .zkconst import *
from struct import unpack
from odoo import api, fields, models
from odoo import _
from odoo.exceptions import UserError, ValidationError
_logger = logging.getLogger(__name__)
try:
    from zk import ZK, const
except ImportError:
    _logger.error("Please Install pyzk library.")

_logger = logging.getLogger(__name__)


class HrAttendance(models.Model):
    _inherit = 'hr.attendance'

    device_id = fields.Char(string='Biometric Device ID')


class ZkMachine(models.Model):
    _name = 'zk.machine'
    
    name = fields.Char(string='Machine IP', required=True)
    port_no = fields.Integer(string='Port No', required=True)
    address_id = fields.Many2one('res.partner', string='Working Address')
    company_id = fields.Many2one('res.company', string='Company', default=lambda self: self.env.user.company_id.id)

    def connection_test(self):
        conn = None
        print('Connecting to the device')
        zk = ZK(self.name, self.port_no, timeout=5)
        try:
            conn = zk.connect()
            print(conn)
            print("Connection Successful")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': 'Connection Successful',
                    'type': 'success',
                    'sticky': False,
                }
            }
        except:
            print("Connection Failed")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'message': 'Connection Failed',
                    'type': 'danger',
                    'sticky': False,
                }
            }

    def device_connect(self, zk):
        try:
            conn = zk.connect()
            return conn
        except:
            return False

    def clear_attendance(self):
        for info in self:
            try:
                machine_ip = info.name
                zk_port = info.port_no
                timeout = 30
                try:
                    zk = ZK(machine_ip, port=zk_port, timeout=timeout, password=0, force_udp=False, ommit_ping=False)
                except NameError:
                    raise UserError(_("Please install it with 'pip3 install pyzk'."))
                conn = self.device_connect(zk)
                if conn:
                    conn.enable_device()
                    clear_data = zk.get_attendance()
                    if clear_data:
                        # conn.clear_attendance()
                        self._cr.execute("""delete from zk_machine_attendance""")
                        conn.disconnect()
                        raise UserError(_('Attendance Records Deleted.'))
                    else:
                        raise UserError(_('Unable to clear Attendance log. Are you sure attendance log is not empty.'))
                else:
                    raise UserError(
                        _('Unable to connect to Attendance Device. Please use Test Connection button to verify.'))
            except:
                raise ValidationError(
                    'Unable to clear Attendance log. Are you sure attendance device is connected & record is not empty.')

    def getSizeUser(self, zk):
        """Checks a returned packet to see if it returned CMD_PREPARE_DATA,
        indicating that data packets are to be sent

        Returns the amount of bytes that are going to be sent"""
        command = unpack('HHHH', zk.data_recv[:8])[0]
        if command == CMD_PREPARE_DATA:
            size = unpack('I', zk.data_recv[8:12])[0]
            print("size", size)
            return size
        else:
            return False

    def zkgetuser(self, zk):
        """Start a connection with the time clock"""
        try:
            users = zk.get_users()
            print(users)
            return users
        except:
            return False

    @api.model
    def cron_download(self):
        machines = self.env['zk.machine'].search([])
        for machine in machines :
            machine.download_attendance()
        
    def download_attendance(self):
        _logger.info("++++++++++++Cron Executed++++++++++++++++++++++")
        zk_attendance = self.env['zk.machine.attendance']
        att_obj = self.env['hr.attendance']
        for info in self:
            machine_ip = info.name
            zk_port = info.port_no
            timeout = 15
            try:
                zk = ZK(machine_ip, port=zk_port, timeout=timeout, password=0, force_udp=False, ommit_ping=False)
            except NameError:
                raise UserError(_("Pyzk module not Found. Please install it with 'pip3 install pyzk'."))
            conn = self.device_connect(zk)
            if conn:
                # conn.disable_device() #Device Cannot be used during this time.
                try:
                    user = conn.get_users()
                except:
                    user = False
                try:
                    attendance = conn.get_attendance()
                except:
                    attendance = False
                if attendance:
                    sorted_attendance = sorted(attendance, key=lambda x: x.timestamp)
                    for each in sorted_attendance:
                        atten_time = each.timestamp
                        atten_time = datetime.strptime(atten_time.strftime('%Y-%m-%d %H:%M:%S'), '%Y-%m-%d %H:%M:%S')
                        local_tz = pytz.timezone(
                            self.env.user.partner_id.tz or 'GMT')
                        local_dt = local_tz.localize(atten_time, is_dst=None)
                        utc_dt = local_dt.astimezone(pytz.utc)
                        utc_dt = utc_dt.strftime("%Y-%m-%d %H:%M:%S")
                        atten_time = datetime.strptime(
                            utc_dt, "%Y-%m-%d %H:%M:%S")
                        atten_time = fields.Datetime.to_string(atten_time)
                        atten_date = datetime.strptime(atten_time, "%Y-%m-%d %H:%M:%S").date()
                        if user:
                            for uid in user:
                                if uid.user_id == each.user_id:
                                    get_user_id = self.env['hr.employee'].search(
                                        [('device_id', '=', each.user_id)])
                                    if get_user_id:
                                        duplicate_atten_ids = zk_attendance.search(
                                            [('device_id', '=', each.user_id), ('punching_time', '=', atten_time)])
                                        if duplicate_atten_ids:
                                            continue
                                        else:
                                            zk_attendance.create({'employee_id': get_user_id.id,
                                                                  'device_id': each.user_id,
                                                                  'attendance_type': str(each.status),
                                                                  'punch_type': str(each.punch),
                                                                  'punching_time': atten_time,
                                                                  'address_id': info.address_id.id})
                                            previous_attendance=att_obj.search([('employee_id','=',get_user_id.id),('check_out','=',False),('check_in','<',atten_time)])
                                            if previous_attendance:
                                                for pa in previous_attendance:
                                                    print(pa.check_in.date())
                                                    print(atten_date)
                                                    if pa.check_in.date() < atten_date:
                                                        pa.write({
                                                            'active':False,
                                                        })
                                            date_obtained =atten_date
                                            date_obtained_start = fields.Datetime.to_string(fields.Datetime.from_string(
                                                str(date_obtained)))  # Convert date to datetime
                                            date_obtained_end = fields.Datetime.to_string(
                                                fields.Datetime.from_string(str(date_obtained)) + timedelta(
                                                    days=1))  # Next day
                                            today_checkin = att_obj.search(
                                                [('employee_id', '=', get_user_id.id),
                                                 ('check_in', '>=', date_obtained_start),
                                                 ('check_in', '<', date_obtained_end)])
                                            if today_checkin:
                                                atten_time_datetime = datetime.strptime(atten_time, "%Y-%m-%d %H:%M:%S")
                                                print(today_checkin.check_in)
                                                print(atten_time_datetime)
                                                if today_checkin.check_in > atten_time_datetime:
                                                    today_checkin.write({
                                                        'check_in':atten_time,
                                                    })
                                                elif today_checkin.check_in < atten_time_datetime:
                                                    check_out_time=today_checkin.check_out
                                                    if check_out_time:
                                                        if today_checkin.check_out < atten_time_datetime:
                                                            today_checkin.write({
                                                                'check_out':atten_time,
                                                            })
                                                    else:
                                                        today_checkin.write({
                                                            'check_out':atten_time,
                                                        })

                                            else:
                                                att_obj.create({
                                                    'employee_id':get_user_id.id,
                                                    'check_in':atten_time
                                                })
                                    else:
                                        employee = self.env['hr.employee'].create(
                                            {'device_id': each.user_id, 'name': uid.name})
                                        zk_attendance.create({'employee_id': employee.id,
                                                              'device_id': each.user_id,
                                                              'attendance_type': str(each.status),
                                                              'punch_type': str(each.punch),
                                                              'punching_time': atten_time,
                                                              'address_id': info.address_id.id})
                                        att_obj.create({'employee_id': employee.id,
                                                        'check_in': atten_time})
                                        
                                else:
                                    pass
                    # zk.enableDevice()
                    conn.disconnect
                    return True
                else:
                    raise UserError(_('Unable to get the attendance log, please try again later.'))
            else:
                raise UserError(_('Unable to connect, please check the parameters and network connections.'))
