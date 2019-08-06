from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

from controller.database import db_controller
from controller.food import food_controller
from controller.log import log_controller
from controller.weight import weight_controller
import pkg.config as config
import shared

app = Flask("Nutrition Mate")
bootstrap = Bootstrap(app)
app.register_blueprint(db_controller)
app.register_blueprint(weight_controller)
app.register_blueprint(food_controller)
app.register_blueprint(log_controller)
# TODO: register log

@app.route("/log")
def log_handler():
    return render_template("log.html", active_page="log")

@app.route("/meals")
def meals_handler():
    return render_template("meals.html", active_page="meals")

@app.route("/")
def home_handler():
    return render_template("home.html", active_page="home")

def init():
    config.load_config("conf/config.ini")
    shared.init()

if __name__ == "__main__":
    init()
    app.run(host=config.values["server"]["host"], port=config.values["server"]["port"])
