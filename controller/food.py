from datetime import datetime

from flask import Blueprint, render_template, request, abort, redirect

import model.food as _food
import pkg.config as config
from pkg.db import DB

food_controller = Blueprint("food_controller", __name__)


@food_controller.route("/food/<name>")
def food_handler(name):
    db = DB(
            config.values["mysql"]["username"],
            config.values["mysql"]["password"],
            config.values["mysql"]["host"],
            config.values["mysql"]["database"]
            )
    try:
        food = _food.get_food(db, config.values["mysql"]["food_table"], name)
        return render_template("food.html", food=food)
    except Exception as e:
        # TODO: handle correctly
        print(e)
        return redirect("/")
