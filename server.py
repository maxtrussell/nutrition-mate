import pkg.config.config as config

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

from pkg.db.db import DB
from model.food.food import Food

app = Flask("Nutrition Mate")
bootstrap = Bootstrap(app)

@app.route("/database")
def database_handler():
    return render_template("database.html", active_page="database")

@app.route("/log")
def log_handler():
    return render_template("log.html", active_page="log")

@app.route("/weight")
def weight_handler():
    return render_template("weight.html", active_page="weight")

@app.route("/")
def home_handler():
    return render_template("home.html", active_page="home")

def init():
    config.load_config("conf/config.ini")
    food = Food(
        name="Apple",
        calories=52.0,
        fat=0.2,
        carbs=14.0,
        protein=0.3,
        sugar=10.0,
        fiber=2.4,
        servings={"100g": 100, "1 medium": 182},
        user="maxtrussell"
    )
    db = DB(
            config.values["mysql"]["username"],
            config.values["mysql"]["password"],
            config.values["mysql"]["host"],
            config.values["mysql"]["database"]
    )
    food.insert(db, "food")

if __name__ == "__main__":
    init()
    app.run(host=config.values["server"]["host"], port=config.values["server"]["port"])
