from flask import (
    Blueprint,
    render_template,
    request,
    flash,
)
from flask_login import current_user, login_required

import app.model.user as _user
from app.pkg.config import Config
from app.pkg.db import get_db
from app.view.preferences_form import PreferencesForm

preferences_bp = Blueprint("preferences_bp", __name__)
config = Config()

@preferences_bp.route("/preferences", methods=["GET", "POST"])
@login_required
def preferences_handler():
    form = PreferencesForm()
    user = _user.get_user_by_username(get_db(config), config.db.USERS, current_user.username)
    if request.method == "GET":
        form.set_fields(user)
    if request.method == "POST":
        form.validate_on_submit()
        for key, val in request.form.items():
            if key not in user.__dict__:
                continue
            elif key == "view_verified_foods":
                # bool type
                user.__setattr__(key, bool(val))
            elif key == "usda_api_key":
                # string type
                user.__setattr__(key, val)
            elif not val:
                # None type
                user.__setattr__(key, None)
            else:
                # float type
                user.__setattr__(key, int(val))
        if "view_verified_foods" not in request.form:
            user.view_verified_foods = False
        user.update(get_db(config), config.db.USERS)
        flash("Successfully updated preferences!")
    return render_template("preferences.html", form=form)
