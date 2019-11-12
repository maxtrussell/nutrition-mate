from flask import Flask, render_template_string
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_flatpages import FlatPages

import markdown

login = LoginManager()
login.login_view = "login_bp.login"
bootstrap = Bootstrap()
flatpages = FlatPages()


def create_app():
    app = Flask(__name__)
    app.config.from_object(__name__)
    app.config['SECRET_KEY'] = 'you-will-never-guess'
    app.config.update({
        'FLATPAGES_ROOT': 'blog',
        'FLATPAGES_EXTENSION': ['.md', '.markdown'],
        'FLATPAGES_MARKDOWN_EXTENSIONS': ['codehilite', 'fenced_code'],
        'FLATPAGES_HTML_RENDERER': renderer
        })

    login.init_app(app)
    bootstrap.init_app(app)
    flatpages.init_app(app)

    return app

def renderer(text):
   rendered_body = render_template_string(text)
   return markdown.markdown(rendered_body, extensions=['codehilite', 'fenced_code'])
