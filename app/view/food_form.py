from flask_wtf import FlaskForm
import json
import re
from wtforms import StringField, PasswordField, BooleanField, SubmitField, FloatField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo

import app.model.user as _user
from app.pkg.config import Config
from app.pkg.db import get_db

config = Config()

class FoodForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    servings = StringField("Servings")
    calories = FloatField("Calories", validators=[DataRequired()])
    fat = FloatField("Fat")
    carbs = FloatField("Carbs")
    protein = FloatField("Protein")
    alcohol = FloatField("Alcohol")
    sugar = FloatField("Sugar")
    fiber = FloatField("Fiber")
    quantity = FloatField("Quantity", validators=[DataRequired()])
    submit = SubmitField("Confirm")

    def validate_servings(self, servings):
        p = "^([a-zA-Z0-9 ]*:[ ]*[\d\.]+,[ ]*)*[a-zA-Z0-9 ]*:[ ]*[\d\.]+[ ]*$"
        match = re.fullmatch(p, servings.data)
        if not match:
            raise ValidationError("Servings field is not valid.")
        

    def set_fields(self, food):
        self.name.data = food.name
        self.servings.data = food.serving_string()
        self.calories.data = food.calories
        self.fat.data = food.fat
        self.carbs.data = food.carbs
        self.protein.data = food.protein
        self.alcohol.data = food.alcohol
        self.sugar.data = food.sugar
        self.fiber.data = food.fiber
        self.quantity.data = 100.0
