import pkg.config.config as config

from flask import Flask
from flask import render_template
from flask_bootstrap import Bootstrap

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

if __name__ == "__main__":
    init()
    app.run(host=config.values["server"]["host"], port=config.values["server"]["port"])
