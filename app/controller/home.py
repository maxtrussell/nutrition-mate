from flask import Blueprint, render_template
from flask_login import current_user

home_bp = Blueprint("home_bp", __name__)

@home_bp.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Nutrition Mate", current_user=current_user)
