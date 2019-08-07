from datetime import date, datetime

from flask import Blueprint, render_template, request, abort, redirect
from flask_login import login_required

from controller.routes import food_controller
import model.food as _food
import pkg.config as config
import shared

@food_controller.route("/food/<name>")
@login_required
def food_handler(name):
    try:
        food = _food.get_food(shared.db, config.values["mysql"]["food_table"], name)
        return render_template("food.html", food=food, date=date.today())
    except Exception as e:
        # TODO: handle correctly
        print(e)
        return redirect("/")
