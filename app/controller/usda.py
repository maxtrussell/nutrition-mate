from ast import literal_eval
from flask import Blueprint, render_template, request, flash, redirect, url_for, Markup
from flask_login import current_user, login_required
import requests
import typing as t

import app.model.food as _food
from app.pkg.config import Config, get_secrets
from app.pkg.db import get_db

usda_bp = Blueprint("usda_bp", __name__)
config = get_secrets(Config())

BASE_URL = "https://api.nal.usda.gov"
SEARCH_PATH = "/fdc/v1/search"
FOOD_DETAIL_PATH = "/fdc/v1/{}"
API_KEY = config.secrets.USDA_API_KEY

FOOD_NUTRIENTS = {
    1003: 'protein',
    1005: 'carbs',
    1004: 'fat',
    1008: 'calories',
    1018: 'alcohol',
    1079: 'fiber',
    2000: 'sugar',
}

@usda_bp.route("/usda/search", methods=["GET"])
@login_required
def usda_search():
    query = request.args.get("query")
    datatypes = []

    datatypes.append(request.args.get("foundation", None))
    datatypes.append(request.args.get("survey", None))
    datatypes.append(request.args.get("branded", None))
    datatypes.append(request.args.get("srlegacy", None))
    datatypes = [dt for dt in datatypes if dt]

    results = _search(query, datatypes)
    return render_template(
            "usda.html",
            title="USDA",
            results=results[:10],
            query=query,
            datatypes=datatypes)

@usda_bp.route("/usda/detail", methods=["GET"])
@login_required
def usda_get_food():
    result = _get_food(request.args.get("fdcID"))
    food = _parse_food(result)
    return render_template("usda_detail.html", title="USDA", food=food)

@usda_bp.route("/usda/save", methods=["POST"])
@login_required
def usda_save_food():
    try:
        food = _food.Food()
        food.user = current_user.username
        servings = literal_eval(request.form.get("servings"))
        for attr, val in request.form.items():
            if attr == "servings":
                food.__setattr__(attr, literal_eval(val))
            else:
                food.__setattr__(attr, val)
        food.id = food.insert(get_db(config), config.db.FOODS)
        food_link = f'<a href="/food/{food.id}">{food.name}</a>'
        flash(Markup(f"Sucessfully added '{food_link}' from USDA!"))
    except Exception as e:
        flash(f"Failed to add food from USDA")
    return redirect(url_for("db_bp.database_handler"))

class SearchResult():
    def __init__(self, result: t.Dict):
        self.description = result["description"]
        self.id = result["fdcId"]
        self.data = result

def _parse_food(usda_food: t.Dict):
    food = _food.Food()
    # parse name
    food.name = usda_food["description"]

    # parse servings
    servings = {"1g": 1, "100g": 100}
    for portion in usda_food["foodPortions"]:
        portion_description = portion.get("portionDescription")
        if not portion_description:
            portion_description = str(int(portion.get("amount"))) + " " +  portion.get("modifier")

        if not portion_description or portion_description == "Quantity not specified":
            continue
        servings[portion_description] = portion["gramWeight"]
    food.servings = servings

    # parse nutrition info
    for nutrient in usda_food["foodNutrients"]:
        nutrient_id = nutrient["nutrient"]["id"]
        if nutrient_id in FOOD_NUTRIENTS:
            food.__setattr__(FOOD_NUTRIENTS[nutrient_id], nutrient["amount"])
    return food

# Sends search to USDA API
def _search(food_name: str, datatypes: t.List[str]):
    if len(datatypes) == 0:
        datatypes.append("Survey (FNDDS)")
    data = {'generalSearchInput': food_name}
    endpoint = BASE_URL + SEARCH_PATH
    params = {"api_key": API_KEY}
    r = requests.post(endpoint, json=data, params=params)
    r.raise_for_status()
    results = []
    for food in r.json()["foods"]:
        if food["dataType"] in datatypes:
            results.append(SearchResult(food))
    return results

# Gets food by fdc id
def _get_food(fdc_id: int):
    endpoint = BASE_URL + FOOD_DETAIL_PATH.format(fdc_id)
    params = {"api_key": API_KEY}
    r = requests.get(endpoint, params=params)
    r.raise_for_status()
    return r.json()
