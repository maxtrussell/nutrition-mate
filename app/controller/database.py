from flask import render_template, request, redirect, flash, Blueprint, url_for, Markup
from flask_login import current_user, login_required

import app.model.food as _food
import app.model.user as _user
from app.pkg.config import Config
from app.pkg.db import get_db

db_bp = Blueprint("db_bp", __name__)
config = Config()

@db_bp.route("/database", methods=["GET"])
@login_required
def database_handler():
    username = current_user.username
    user = _user.get_user_by_username(get_db(config), config.db.USERS, current_user.username)
    query = request.args.get("query", default="")
    if query:
        foods = _food.search(
            get_db(config), config.db.FOODS, query.lower(), username, user.view_verified_foods
        )
    else:
        foods = _food.get_all_foods(get_db(config), config.db.FOODS, username, user.view_verified_foods)
    return render_template(
        "database.html", active_page="database", foods=foods, query=query, user=user
    )


@db_bp.route("/database/clear", methods=["GET"])
@login_required
def database_clear_handler():
    return redirect("/database")


@db_bp.route("/database/delete/<int:id>", methods=["GET"])
@login_required
def database_delete_handler(id):
    try:
        user = _user.get_user_by_username(get_db(config), config.db.USERS, current_user.username)
        food = _food.get_food(get_db(config), config.db.FOODS, id, current_user.username, user.view_verified_foods)
        if user.username != food.user:
            flash("You do not have edit permissions for this item.")
            return redirect(url_for("food_bp.food_handler", id=id))
        _food.delete_by_id(
            get_db(config), config.db.FOODS, id, current_user.username)
        flash("Successfully deleted food")
    except Exception as e:
        flash("Failed to delete food: {}".format(e))
    return redirect(url_for("db_bp.database_handler"))


@db_bp.route("/database/add", methods=["POST"])
@login_required
def database_add_handler():
    try:
        if request.form["name"] == "" or request.form["quantity"] == "":
            raise Exception("food requires 'name' and 'quantity'")

        parsed = {}
        for key, value in request.form.items():
            key, value = key.strip(), value.strip()
            if key == "servings":
                parsed[key] = _food.parse_servings(value)
            elif key == "name":
                parsed[key] = value
            elif value == "":
                parsed[key] = 0.0
            else:
                parsed[key] = float(value)

        food = _food.Food(
                name=parsed["name"], calories=parsed["calories"], fat=parsed["fat"],
                carbs=parsed["carbs"], protein=parsed["protein"],
                alcohol=parsed["alcohol"], sugar=parsed["sugar"], fiber=parsed["fiber"],
                user=current_user.username, servings=parsed["servings"]
                )
        food = food.normalize(current=parsed["quantity"])

        food.id = food.insert(get_db(config), config.db.FOODS)
        food_link = f'<a href="/food/{food.id}">{food.name}</a>'
        flash(Markup(f"Successfully added food '{food_link}'"))
    except Exception as e:
        flash("Failed to add food '{}': {}".format(food.name, e))
    finally:
        return redirect("/database")
