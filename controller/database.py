from flask import render_template, request, abort, redirect
from flask_login import login_required

from controller.routes import db_controller
import model.food as _food
import pkg.config as config
import shared

@db_controller.route("/database", methods=["GET"])
@login_required
def database_handler():
    query = request.args.get("query", default="")
    if query:
        foods = _food.search(shared.db, config.values["mysql"]["food_table"], query.lower())
    else:
        foods = _food.get_all_foods(shared.db, config.values["mysql"]["food_table"])
    return render_template("database.html", active_page="database", foods=foods, query=query)

@db_controller.route("/database/clear", methods=["GET"])
@login_required
def database_clear_handler():
    return redirect("/database")

@db_controller.route("/database/delete", methods=["POST"])
@login_required
def database_delete_handler():
    try:
        name = request.form["name"]
        _food.delete_by_name(shared.db, config.values["mysql"]["food_table"], name)
    except Exception as e: 
        # TODO: add banner message on error
        print("failed to delete food")
        print(e)
    finally:
        return redirect("/database")
        

@db_controller.route("/database/add", methods=["POST"])
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
                user="maxtrussell", servings=parsed["servings"]
                )
        food = food.normalize(current=parsed["quantity"])

        food.insert(shared.db, config.values["mysql"]["food_table"])
    except Exception as e: 
        # TODO: add banner message on error
        print("failed to add food")
        print(e)
    finally:
        return redirect("/database")
