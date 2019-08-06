from datetime import datetime

from flask import Blueprint, render_template, request, abort, redirect

import model.weight as _weight
import pkg.config as config
import shared

weight_controller = Blueprint("weight_controller", __name__)


@weight_controller.route("/weight")
def weight_handler():
    dt = datetime.now()
    date = dt.strftime("%Y-%m-%d")
    weights = _weight.get_last_weights(shared.db, config.values["mysql"]["weight_table"])
    return render_template("weight.html", active_page="weight", date=date, weights=weights)

@weight_controller.route("/weight/add", methods=["POST"])
def weight_add_handler():
    try:
        if request.form["weight"] == "" or request.form["log_date"] == "":
            raise Exception("weight requires 'weight' and 'date'")
        weight = _weight.Weight(float(request.form["weight"]))
        weight.date = datetime.strptime(request.form["log_date"], "%Y-%m-%d")
        weight.notes = request.form["notes"]
        weight.insert(shared.db, config.values["mysql"]["weight_table"])
    except Exception as e:
        print(e)
    finally:
        return redirect("/weight")

@weight_controller.route("/weight/delete/<date>", methods=["GET"])
def weight_delete_handler(date):
    date = datetime.strptime(date, "%Y-%m-%d")
    _weight.delete_by_date(shared.db, config.values["mysql"]["weight_table"], date)
    return redirect("/weight")
