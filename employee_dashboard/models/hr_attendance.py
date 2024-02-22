from odoo import api,models,fields

class AttendanceInherit(models.Model):
    _inherit = "hr.attendance"

    checkin_address = fields.Char(string='Check In Address', store=True,
                                  help="Check in address of the User")
    checkout_address = fields.Char(string='Check Out Address', store=True,
                                   help="Check out address of the User")
    checkin_latitude = fields.Char(string='Check In Latitude', store=True,
                                   help="Check in latitude of the User")
    checkout_latitude = fields.Char(string='Check Out Latitude', store=True,
                                    help="Check out latitude of the User")
    checkin_longitude = fields.Char(string='Check In Longitude', store=True,
                                    help="Check in longitude of the User")
    checkout_longitude = fields.Char(string='Check Out Longitude', store=True,
                                     help="Check out longitude of the User")
    checkin_location = fields.Char(string='Check In Location Link', store=True,
                                   help="Check in location link of the User")
    checkout_location = fields.Char(string='Check Out Location Link', store=True,
                                    help="Check out location link of the User")
    active=fields.Boolean(string="Active", default=True)
    proof_checkin=fields.Binary(string="CheckIn Proof",store=True)
    proof_checkout=fields.Binary(string="CheckOut Proof",store=True)