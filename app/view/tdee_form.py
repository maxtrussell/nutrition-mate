from flask_wtf import FlaskForm
from wtforms import (
    RadioField,
    IntegerField,
    DecimalField,
    SelectField,
    SubmitField,
)
from wtforms.validators import optional, InputRequired

class TdeeForm(FlaskForm):
    activity_levels = [
        ("Sedentary (office job)", "Sedentary (office job)"),
        ("Light Exercise (1-2 days/week)", "Light Exercise (1-2 days/week)"),
        ("Moderate Exercise (3-5 days/week)", "Moderate Exercise (3-5 days/week)"),
        ("Heavy Exercise (6-7 days/week)", "Heavy Exercise (6-7 days/week)"),
        ("Athlete (2x per day)", "Athlete (2x per day)"),
    ]
    gender = RadioField("Gender", choices=[("Male", "Male"), ("Female", "Female")], default="Male")
    age = IntegerField("Age", [InputRequired()])
    height = IntegerField("Height (inches or centimeters)", [InputRequired()])
    weight = DecimalField("Weight", [InputRequired()])
    activity = SelectField("Activity Level", [InputRequired()], choices=activity_levels)
    weight_delta = DecimalField("Desired weight change per week", [optional()])
    units = RadioField("Units", [InputRequired()], choices=[("imperial", "imperial"), ("metric", "metric")], default="imperial")
    submit = SubmitField("Calculate")
