from flask import g
from flask_httpauth import HTTPBasicAuth, HTTPTokenAuth
from flask_login import current_user

import app.model.user as _user
from app.api.errors import error_response
from app.pkg.config import Config, get_secrets
from app.pkg.db import get_db

config = get_secrets(Config())

basic_auth = HTTPBasicAuth()
token_auth = HTTPTokenAuth()

@basic_auth.verify_password
def verify_password(username: str, password: str):
    user = _user.get_user_by_username(get_db(config), config.db.USERS, username)
    if user is None:
        return False
    g.current_user = user
    return user.check_password(password)

@basic_auth.error_handler
def basic_auth_error():
    return error_response(401)
