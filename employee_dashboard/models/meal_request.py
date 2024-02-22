from odoo import models,api,fields
class MealRequest(models.Model):
    _name = 'meal.request'
    _description = 'Meal Request'

    employee_id = fields.Many2one('hr.employee', string='Employee', required=True)

    meal_time = fields.Selection([
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
        ('breakfast', 'Breakfast'),
        ('snacks', 'Snacks'),
    ], string='Meal Type', required=True)
    day_of_week = fields.Selection([
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
    ], string='Day of the Week', required=True)
    requested_date = fields.Date(string='Requested Date', required=True, default=fields.Date.today())
    food_id = fields.Many2many('food.name' ,string='Food')
    state = fields.Selection([
        ('Attending', 'Attending'),
        ('Not Attending', 'Not Attending'),
    ], string='Status', default='Attending')

    @api.model
    def get_attendance_counts(self):
        attending_count = self.search_count([('state', '=', 'Attending')])
        not_attending_count = self.search_count([('state', '=', 'Not Attending')])

        return {
            'attending_count': attending_count,
            'not_attending_count': not_attending_count,
        }