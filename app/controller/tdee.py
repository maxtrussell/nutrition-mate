from enum import Enum

from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    Markup,
)

from app.pkg.config import Config
from app.pkg.db import get_db
from app.view.tdee_form import TdeeForm

tdee_bp = Blueprint("tdee_bp", __name__)
config = Config()

@tdee_bp.route("/tdee", methods=["GET", "POST"])
def tdee_handler():
    form = TdeeForm()
    tdee = None
    bmr = None
    daily_calories = None
    if request.method == "POST":
        if not form.validate_on_submit():
            return render_template("tdee.html", form=form, tdee=tdee, bmr=bmr, daily_calories=daily_calories)

        weight = float(request.form.get("weight"))
        height = int(request.form.get("height"))
        weight_delta = request.form.get("weight_delta", 0.0)
        weight_delta = 0.0 if weight_delta == "" else float(weight_delta)
        if request.form.get("units") == "imperial":
            weight *= 0.453592
            weight_delta *= 0.453592
            height *= 2.54

        # parse gender
        gender = Gender.MALE
        if request.form.get("gender") == "Female":
            gender = Gender.FEMALE
        
        # parse activity level
        value = request.form.get("activity")
        if value == "Sedentary (office job)":
            activity_level = ActivityLevel.SEDENTARY
        elif value == "Light Exercise (1-2 days/week)":
            activity_level = ActivityLevel.LIGHT
        elif value == "Moderate Exercise (3-5 days/week)":
            activity_level = ActivityLevel.MODERATE
        elif value == "Heavy Exercise (6-7 days/week)":
            activity_level = ActivityLevel.HEAVY
        else:
            activity_level = ActivityLevel.EXTRA

        bmr = _bmr(
                gender,
                int(request.form.get("age")),
                weight,
                height,
            )
        tdee = _tdee(bmr, activity_level)
        if request.form.get("weight_delta"):
            daily_calories = _daily_calories(weight_delta, tdee)
        else:
            daily_calories = tdee

        flash(
            f"<b>Results:</b>\n"
            f"<ul>\n"
            f"<li>BMR: {bmr}</li>\n"
            f"<li>TDEE: {tdee}</li>\n"
            f"<li>Daily Caloric Target: {daily_calories}</li>\n"
            f"</ul>"
        )
    return render_template("tdee.html", form=form)

class ActivityLevel(Enum):
    SEDENTARY = 1.2
    LIGHT = 1.375
    MODERATE = 1.55
    HEAVY = 1.725
    EXTRA = 1.9

class Gender(Enum):
    MALE = 1
    FEMALE = 2

def _daily_calories(
        weight_delta: float,
        tdee: int
    ):
    # there are 7716 calories / kilogram of fat
    return int(tdee + weight_delta * 7716 / 7)

def _tdee(
        bmr: int,
        activity_level: ActivityLevel,
    ) -> int:
    return int(bmr * activity_level.value)


def _bmr(
        gender: Gender,
        age: int,
        weight: float,
        height: int,
    ):
    """
    Returns the BMR
    Uses Harris-Benedict formula
    """
    bmr = -1  # bmr is defined as kcal/day
    if gender == Gender.MALE:
        bmr = ((13.397 * weight) + (4.799 * height) -
                (5.677 * age) + 88.32)
    elif gender == Gender.FEMALE:
        bmr = ((9.247 * weight) + (3.098 * height) -
                (4.330 * age) + 447.595)
    return int(bmr)

