from datetime import date

from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import current_user, login_required

import app.model.food as _food
import app.model.user as _user
from app.pkg.config import Config
from app.pkg.db import get_db
from app.view.food_form import FoodForm

food_bp = Blueprint("food_bp", __name__)
config = Config()

@food_bp.route("/food/<id>")
@login_required
def food_handler(id):
    user = _user.get_user_by_username(get_db(config), config.db.USERS, current_user.username)
    serving = request.args.get("serving", default="100g")
    try:
        food = _food.get_food(get_db(config), config.db.FOODS, id, current_user.username, user.view_verified_foods)
        if serving:
            if serving not in food.servings:
                flash(f"No such serving '{serving}' for food '{food.name}'.")
                return redirect(url_for("food_bp.food_handler", id=id))
            serving_size = food.servings[serving]
            food = food.normalize(target=serving_size)
        return render_template("food.html", food=food, date=date.today(), selected_serving=serving, user=user)
    except Exception as e:
        flash("Could not get food: {}".format(e))
        return redirect(url_for("home_bp.index"))

@food_bp.route("/food/edit/<int:id>", methods=["GET", "POST"])
@login_required
def edit(id):
    form = FoodForm()
    food = _food.Food()
    try:
        user = _user.get_user_by_username(get_db(config), config.db.USERS, current_user.username)
        food = _food.get_food(get_db(config), config.db.FOODS, id, current_user.username, user.view_verified_foods)
        if user.username != food.user:
            flash("You do not have edit permissions for this item.")
            return redirect(url_for("food_bp.food_handler", id=id))
    except Exception as e:
        flash("Could not get food: {}".format(e))
        return redirect(url_for("home_bp.index"))
    if request.method == "GET":
        form.set_fields(food)
    if form.validate_on_submit():
        food.name = form.name.data
        food.servings = _food.parse_servings(form.servings.data)
        # Ensure 1g and 100g serving sizes exist
        food.servings["1g"] = 1
        food.servings["100g"] = 100
        food.calories = form.calories.data
        food.fat = form.fat.data
        food.carbs = form.carbs.data
        food.protein = form.protein.data
        food.alcohol = form.alcohol.data
        food.sugar = form.sugar.data
        food.fiber = form.fiber.data
        food.quantity = form.quantity.data
        food.id = id
        food.username = current_user.username
        food.update(get_db(config), config.db.FOODS)
        flash("Successfully updated '{}'".format(food.name))
        return redirect(url_for("food_bp.food_handler", id=id))
    else:
        return render_template("food_edit.html", title="Edit", form=form, food=food)
    
