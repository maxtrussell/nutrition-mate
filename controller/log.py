from datetime import date, datetime

from flask import render_template, request, abort, redirect, url_for
from flask_login import current_user, login_required

from controller.routes import log_controller
import model.food as _food
import model.log as _log
import pkg.config as config
from pkg.utils import toDate, toTime
import shared

@log_controller.route("/log")
@login_required
def log_handler():
    selected_date = request.args.get("selectedDate", default=date.today(), type=toDate)
    entries = _log.get_entries_by_day(
            shared.db, 
            config.values["mysql"]["log_table"], 
            config.values["mysql"]["food_table"], 
            selected_date,
            current_user.username
            )

    # generate daily sums
    calorieSum, fatSum, carbsSum, proteinSum, sugarSum, fiberSum, alcoholSum = 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    for entry in entries:
        calorieSum += entry.food.calories
        fatSum += entry.food.fat
        carbsSum += entry.food.carbs
        proteinSum += entry.food.protein
        sugarSum += entry.food.sugar
        fiberSum += entry.food.fiber
        alcoholSum += entry.food.alcohol

    return render_template(
            "log.html", active_page="log", selectedDate=selected_date, entries=entries,
            calorieSum=calorieSum, proteinSum=proteinSum, sugarSum=sugarSum, fiberSum=fiberSum,
            fatSum=fatSum, carbsSum=carbsSum, alcoholSum=alcoholSum
            )

@log_controller.route("/log/add", methods=["POST"])
def log_add_handler():
    selected_date = request.form.get("selectedDate", default=None)
    id = request.form.get("id")
    serving = request.form.get("serving")
    quantity = request.form.get("quantity", type=float)
    username = current_user.username

    food = _food.get_food(shared.db, config.values["mysql"]["food_table"], id, username)
    
    entry = _log.LogEntry(
            food, id=food.id, time=selected_date, quantity=quantity, serving=serving,
            username=username
            )
    entry.insert(shared.db, config.values["mysql"]["log_table"])
    return redirect(url_for("log_controller.log_handler", selectedDate=selected_date))

@log_controller.route("/log/delete/<id>", methods=["GET"])
def log_delete_handler(id):
    _log.delete_entry(shared.db, config.values["mysql"]["log_table"], id)
    selected_date = request.args.get("selectedDate", default="")
    if selected_date != "":
        selected_date = toDate(selected_date)
    else:
        selected_date = datetime.now().date()
    return redirect(url_for("log_controller.log_handler", selectedDate=selected_date))

@log_controller.route("/log/search")
def log_search_handler():
    query = request.args.get("query", default="")
    results = _food.search(shared.db, config.values["mysql"]["food_table"], query.lower())
    if len(results) == 1:
        return redirect("/food/{}".format(results[0].name))
    else:
        return redirect(url_for("db_controller.database_handler", query=query))


