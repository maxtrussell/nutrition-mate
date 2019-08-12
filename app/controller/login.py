from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user

import app.model.user as _user
from app.pkg.config import Config, get_secrets
from app.pkg.db import get_db
from app.view.login_form import LoginForm
from app.view.registration_form import RegistrationForm
from app import login

login_bp = Blueprint("login_bp", __name__)
config = get_secrets(Config())

@login.user_loader
def load_user(id):
    return _user.get_user_by_id(get_db(config), config.db.USERS, int(id))

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home_bp.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = _user.get_user_by_username(get_db(config), config.db.USERS, form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login_bp.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for("home_bp.index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)

@login_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home_bp.index"))

@login_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home_bp.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.registration_key.data != config.secrets.REGISTRATION_KEY:
            flash("Incorrect registration key")
            return redirect(url_for("login_bp.register"))

        user = _user.User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.insert(get_db(config), config.db.USERS)
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login_bp.login"))
    return render_template("register.html", title="Register", form=form)
