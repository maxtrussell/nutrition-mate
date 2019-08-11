from flask import Flask
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

login = LoginManager()
login.login_view = "login_bp.login"
bootstrap = Bootstrap()


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'you-will-never-guess'

    login.init_app(app)
    bootstrap.init_app(app)

    return app
