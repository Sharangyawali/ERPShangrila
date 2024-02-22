from odoo import models, fields, api
from odoo.exceptions import ValidationError


class FoodList(models.Model):
    _name = 'food.list'

    food_mapping=fields.Many2one('food.mapping')
    # meal_time = fields.Many2one('meal.time')
    meal_time_ref = fields.Selection([
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Snacks'),
        ('dinner', 'Dinner'),
    ],string='Meal Time')
    meal_name = fields.Many2many('food.name' ,string='Food')



class FoodMapping(models.Model):
    _name = 'food.mapping'
    _rec_name = 'day_of_week'

    day_of_week = fields.Selection([
        ('sunday', 'Sunday'),
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
    ], string='Day of the Week', required=True)

    food_list_ids = fields.One2many('food.list','food_mapping',String="Food list Ids" )


    @api.constrains('day_of_week')
    def check_duplicate_date(self):
        for rec in self:
            if self.search_count([('day_of_week', '=', rec.day_of_week)]) > 1:
                raise ValidationError("Duplicate day_of_week value found in records.")

class FoodName(models.Model):
    _name = 'food.name'

    name = fields.Char('Food Name')
    food_list_ref=fields.Many2one('food.list')

class MealTime(models.Model):
    _name = 'meal.time'

    name = fields.Selection([
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snacks', 'Snacks'),
        ('dinner', 'Dinner'),
    ],string='Meal Time')