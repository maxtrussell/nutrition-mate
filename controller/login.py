from flask import Blueprint, flash, render_template, request, redirect, url_for
from flask_login import current_user, login_user, logout_user

from controller.routes import login_controller
import model.user as _user
import pkg.config as config
import shared
from view.login_form import LoginForm
from view.registration_form import RegistrationForm

@shared.login.user_loader
def load_user(id):
    return _user.get_user_by_id(shared.db, config.values["mysql"]["user_table"], int(id))

@login_controller.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home_controller.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = _user.get_user_by_username(shared.db, config.values["mysql"]["user_table"], form.username.data)
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login_controller.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page:
            next_page = url_for("home_controller.index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)

@login_controller.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("home_controller.index"))

@login_controller.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("home_controller.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.registration_key.data != config.values["secrets"]["registration_key"]:
            flash("Incorrect registration key")
            return redirect(url_for("login_controller.register"))

        user = _user.User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        user.insert(shared.db, config.values["mysql"]["user_table"])
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login_controller.login"))
    return render_template("register.html", title="Register", form=form)
