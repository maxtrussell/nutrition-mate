from flask import Flask, render_template
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

from pkg.db import DB
import pkg.config as config

db = None
app = Flask(__name__)
# TODO: config
app.config['SECRET_KEY'] = 'you-will-never-guess'
bootstrap = Bootstrap(app)
login = LoginManager(app)
login.login_view = "login_controller.login"

# Sets up mysql connection
def init():
    global db

    db = DB(
            config.values["mysql"]["username"],
            config.values["mysql"]["password"],
            config.values["mysql"]["host"],
            config.values["mysql"]["database"]
            )
