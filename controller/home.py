from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user

from controller.routes import home_controller

@home_controller.route("/", methods=["GET"])
def index():
    return render_template("index.html", title="Nutrition Mate", current_user=current_user)
