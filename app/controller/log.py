from datetime import date, datetime

from flask import render_template, request, redirect, url_for, flash, Blueprint, Markup
from flask_login import current_user, login_required

import app.model.food as _food
import app.model.log as _log
import app.model.user as _user
from app.pkg.config import Config
from app.pkg.utils import toDate
from app.pkg.db import get_db

log_bp = Blueprint("log_bp", __name__)
config = Config()

@log_bp.route("/log")
@login_required
def log_handler():
    selected_date = request.args.get("selectedDate", default=date.today(), type=toDate)
    entries = _log.get_entries_by_day(
            get_db(config), 
            config.db.LOG, 
            config.db.FOODS, 
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
        entry.time = entry.time.strftime("%-I:%M %p")

    # get user goals
    user = _user.get_user_by_username(get_db(config), config.db.USERS, current_user.username)

    return render_template(
            "log.html", active_page="log", user=user, selectedDate=selected_date, entries=entries,
            calorieSum=calorieSum, proteinSum=proteinSum, sugarSum=sugarSum, fiberSum=fiberSum,
            fatSum=fatSum, carbsSum=carbsSum, alcoholSum=alcoholSum
            )

@log_bp.route("/log/add", methods=["POST"])
def log_add_handler():
    selected_date = request.form.get("selectedDate", default=None)
    id = request.form.get("id")
    serving = request.form.get("serving")
    quantity = request.form.get("quantity", type=float)
    username = current_user.username
    user = _user.get_user_by_username(get_db(config), config.db.USERS, username)

    food = _food.get_food(get_db(config), config.db.FOODS, id, username, user.view_verified_foods)

    # if the selected date is today, include hours:minutes
    time = selected_date
    if selected_date == date.today().strftime("%Y-%m-%d"):
        time = datetime.now()
    
    entry = _log.LogEntry(
            food, id=food.id, time=time, quantity=quantity, serving=serving,
            username=username
            )
    entry.insert(get_db(config), config.db.LOG)
    food_link = f'<a href="/food/{id}">{food.name}</a>'
    flash(Markup("Successfully added '{} x {} of {}' to log".format(quantity, serving, food_link)))
    return redirect(url_for("log_bp.log_handler", selectedDate=selected_date))

@log_bp.route("/log/delete/<id>", methods=["GET"])
def log_delete_handler(id):
    user = _user.get_user_by_username(get_db(config), config.db.USERS, current_user.username)
    entry = _log.get_entry_by_id(get_db(config), config.db.LOG, id, user.username)
    if not entry:
        flash("You do not have edit permissions for this item.")
        return redirect(url_for("log_bp.log_handler", id=id))
    _log.delete_entry(get_db(config), config.db.LOG, id)
    selected_date = request.args.get("selectedDate", default="")
    if selected_date != "":
        selected_date = toDate(selected_date)
    else:
        selected_date = datetime.now().date()
    flash("Successfully deleted log entry!")
    return redirect(url_for("log_bp.log_handler", selectedDate=selected_date))

@log_bp.route("/log/search")
def log_search_handler():
    query = request.args.get("query", default="")
    user = _user.get_user_by_username(get_db(config), config.db.USERS, current_user.username)
    results = _food.search(get_db(config), config.db.FOODS, query.lower(), current_user.username, user.view_verified_foods)
    if len(results) == 1:
        return redirect("/food/{}".format(results[0].id))
    elif len(results) == 0:
        flash("No results for food '{}'".format(query))
        return redirect(url_for("log_bp.log_handler"))
    else:
        return redirect(url_for("db_bp.database_handler", query=query))


