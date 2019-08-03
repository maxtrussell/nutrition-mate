from datetime import date, datetime

from flask import Blueprint, render_template, request, abort, redirect, url_for

import model.food as _food
import model.log as _log
import pkg.config as config
from pkg.db import DB
from pkg.utils import toDate, toTime

log_controller = Blueprint("log_controller", __name__)

@log_controller.route("/log")
def log_handler():
    selected_date = request.args.get("selectedDate", default=date.today(), type=toDate)
    db = DB(
        config.values["mysql"]["username"],
        config.values["mysql"]["password"],
        config.values["mysql"]["host"],
        config.values["mysql"]["database"]
        )
    # TODO: rows=logEntries
    entries = _log.get_entries_by_day(
            db, 
            config.values["mysql"]["log_table"], 
            config.values["mysql"]["food_table"], 
            selected_date
            )

    # generate daily sums
    calorieSum, proteinSum, sugarSum, fiberSum = 0.0, 0.0, 0.0, 0.0
    for entry in entries:
        calorieSum += entry.food.calories
        proteinSum += entry.food.protein
        sugarSum += entry.food.sugar
        fiberSum += entry.food.fiber

    return render_template(
            "log.html", active_page="log", selectedDate=selected_date, entries=entries,
            calorieSum=calorieSum, proteinSum=proteinSum, sugarSum=sugarSum, fiberSum=fiberSum
            )

@log_controller.route("/log/add", methods=["POST"])
def log_add_handler():
    db = DB(
        config.values["mysql"]["username"],
        config.values["mysql"]["password"],
        config.values["mysql"]["host"],
        config.values["mysql"]["database"]
        )
    selected_date = request.form.get("selectedDate", default=None)
    name = request.form.get("name")
    serving = request.form.get("serving")
    quantity = request.form.get("quantity", type=float)
    username = request.form.get("username", default="maxtrussell")

    food = _food.get_food(db, config.values["mysql"]["food_table"], name)
    
    entry = _log.LogEntry(food, time=selected_date, quantity=quantity, serving=serving)
    entry.insert(db, config.values["mysql"]["log_table"], )
    return redirect(url_for("log_controller.log_handler", selectedDate=selected_date))

@log_controller.route("/log/delete/<id>", methods=["GET"])
def log_delete_handler(id):
    db = DB(
        config.values["mysql"]["username"],
        config.values["mysql"]["password"],
        config.values["mysql"]["host"],
        config.values["mysql"]["database"]
        )
    _log.delete_entry(db, config.values["mysql"]["log_table"], id)
    selected_date = request.args.get("selectedDate", default="")
    if selected_date != "":
        selected_date = toDate(selected_date)
    else:
        selected_date = datetime.now().date()
    return redirect(url_for("log_controller.log_handler", selectedDate=selected_date))

@log_controller.route("/log/search")
def log_search_handler():
    db = DB(
        config.values["mysql"]["username"],
        config.values["mysql"]["password"],
        config.values["mysql"]["host"],
        config.values["mysql"]["database"]
        )
    query = request.args.get("query", default="")
    results = _food.search(db, config.values["mysql"]["food_table"], query.lower())
    if len(results) == 1:
        return redirect("/food/{}".format(results[0].name))
    else:
        return redirect(url_for("db_controller.database_handler", query=query))


