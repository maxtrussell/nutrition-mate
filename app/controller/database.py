from flask import render_template, request, redirect, flash, Blueprint, url_for
from flask_login import current_user, login_required

import app.model.food as _food
from app.pkg.config import Config
from app.pkg.db import get_db

db_bp = Blueprint("db_bp", __name__)
config = Config()

@db_bp.route("/database", methods=["GET"])
@login_required
def database_handler():
    username = current_user.username
    query = request.args.get("query", default="")
    if query:
        foods = _food.search(
            get_db(config), config.db.FOODS, query.lower(), username)
    else:
        foods = _food.get_all_foods(get_db(config), config.db.FOODS, username)
    return render_template(
        "database.html", active_page="database", foods=foods, query=query)


@db_bp.route("/database/clear", methods=["GET"])
@login_required
def database_clear_handler():
    return redirect("/database")


@db_bp.route("/database/delete/<int:id>", methods=["GET"])
@login_required
def database_delete_handler(id):
    try:
        _food.delete_by_id(
            get_db(config), config.db.FOODS, id, current_user.username)
        flash("Successfully deleted food")
    except Exception as e:
        flash("Failed to delete food: {}".format(e))
    finally:
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

        food.insert(get_db(config), config.db.FOODS)
        flash("Successfully added food '{}'".format(food.name))
    except Exception as e:
        flash("Failed to add food '{}': {}".format(food.name, e))
    finally:
        return redirect("/database")
