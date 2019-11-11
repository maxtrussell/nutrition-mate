from flask_wtf import FlaskForm
from wtforms import IntegerField, BooleanField, SubmitField, StringField
from wtforms.validators import optional

class PreferencesForm(FlaskForm):
    calories_goal = IntegerField("Daily calories target", [optional()])
    fat_goal = IntegerField("Daily fat target", [optional()])
    carbs_goal = IntegerField("Daily carbs target", [optional()])
    protein_goal = IntegerField("Daily protein target", [optional()])
    sugar_goal = IntegerField("Daily sugar target", [optional()])
    fiber_goal = IntegerField("Daily fiber target", [optional()])
    usda_api_key = StringField("USDA API key", [optional()])
    view_verified_foods = BooleanField("View verified foods?")
    submit = SubmitField("Save")

    def set_fields(self, user):
        self.calories_goal.data = user.calories_goal
        self.fat_goal.data = user.fat_goal
        self.carbs_goal.data = user.carbs_goal
        self.protein_goal.data = user.protein_goal
        self.sugar_goal.data = user.sugar_goal
        self.fiber_goal.data = user.fiber_goal
        self.usda_api_key.data = user.usda_api_key
        self.view_verified_foods.data = user.view_verified_foods
