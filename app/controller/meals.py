from flask import (
    Blueprint,
    render_template,
    request,
    flash,
    url_for,
    redirect,
)
from flask_login import (
    login_required,
    current_user,
)

import app.model.meal as _meal
import app.model.user as _user
from app.pkg.config import Config
from app.pkg.db import get_db

meals_bp = Blueprint("meals_bp", __name__)
config = Config()

@meals_bp.route("/meals", methods=["GET", "POST"])
@login_required
def meals_handler():
    if request.method == "POST":
        name = request.form.get("name")
        new_meal =  _meal.Meal(name, current_user.username)
        new_meal.insert(get_db(config), config.db.MEALS)
    query = request.args.get("query", None)
    meals = _meal.get_by_username(get_db(config), config.db.MEALS, current_user.username)
    for meal in meals:
        meal.get_ingredients(get_db(config), config.db.INGREDIENTS, config.db.FOODS)
    return render_template("meals.html", active_page="meals", query=query, meals=meals)

@meals_bp.route("/meals/<id>", methods=["GET"])
@login_required
def meal_handler(id: int):
    meal = _meal.get_by_id(get_db(config), config.db.MEALS, id)
    return render_template("meal.html", meal=meal)
