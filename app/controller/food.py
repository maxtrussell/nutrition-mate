from datetime import date

from flask import Blueprint, render_template, redirect
from flask_login import current_user, login_required

import app.model.food as _food
from app.pkg.config import Config
from app.pkg.db import get_db

food_bp = Blueprint("food_bp", __name__)
config = Config()

@food_bp.route("/food/<id>")
@login_required
def food_handler(id):
    try:
        food = _food.get_food(get_db(config), config.db.FOODS, id, current_user.username)
        return render_template("food.html", food=food, date=date.today())
    except Exception as e:
        # TODO: handle correctly
        print(e)
        return redirect("/")
