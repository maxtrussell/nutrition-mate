from datetime import date, datetime

from flask import Blueprint, render_template, request, abort, redirect

import model.food as _food
import pkg.config as config
import shared

food_controller = Blueprint("food_controller", __name__)


@food_controller.route("/food/<name>")
def food_handler(name):
    try:
        food = _food.get_food(shared.db, config.values["mysql"]["food_table"], name)
        return render_template("food.html", food=food, date=date.today())
    except Exception as e:
        # TODO: handle correctly
        print(e)
        return redirect("/")
