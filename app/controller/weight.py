from datetime import datetime

from flask import render_template, request, redirect, flash, Blueprint, url_for
from flask_login import current_user, login_required

import app.model.weight as _weight
from app.pkg.config import Config
from app.pkg.db import get_db

weight_bp = Blueprint("weight_bp", __name__)
config = Config()

@weight_bp.route("/weight")
@login_required
def weight_handler():
    dt = datetime.now()
    date = dt.strftime("%Y-%m-%d")
    weights = _weight.get_last_weights(
            get_db(config), config.db.WEIGHTS, username=current_user.username
            )
    return render_template("weight.html", active_page="weight", date=date, weights=weights)

@weight_bp.route("/weight/add", methods=["POST"])
@login_required
def weight_add_handler():
    if request.form["weight"] == "" or request.form["log_date"] == "":
        flash("Weight requires 'weight' and 'date'")
    else:
        weight = _weight.Weight(float(request.form["weight"]))
        weight.date = datetime.strptime(request.form["log_date"], "%Y-%m-%d")
        weight.notes = request.form["notes"]
        weight.username = current_user.username
        weight.insert(get_db(config), config.db.WEIGHTS)
        flash("Successfully added weight to log!")
    return redirect(url_for("weight_bp.weight_handler"))

@weight_bp.route("/weight/delete/<id>", methods=["GET"])
@login_required
def weight_delete_handler(id):
    _weight.delete_by_id(get_db(config), config.db.WEIGHTS, id)
    return redirect(url_for("weight_bp.weight_handler"))
