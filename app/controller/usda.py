from flask import Blueprint, render_template, request, flash
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

@usda_bp.route("/usda/search", methods=["GET"])
@login_required
def usda_search():
    query = request.args.get("query")
    results = _search(query)
    return render_template("usda.html", title="USDA", results=results[:10])

@usda_bp.route("/usda/detail", methods=["GET"])
@login_required
def usda_get_food():
    result = _get_food(request.args.get("fdcID"))
    return render_template("usda_detail.html", title="USDA", food=result)

class SearchResult():
    def __init__(self, result: t.Dict):
        self.description = result["description"]
        self.id = result["fdcId"]

# Sends search to USDA API
def _search(food_name: str):
    data = {'generalSearchInput': food_name}
    endpoint = BASE_URL + SEARCH_PATH
    params = {"api_key": API_KEY}
    r = requests.post(endpoint, json=data, params=params)
    r.raise_for_status()
    results = []
    for food in r.json()["foods"]:
        if food["dataType"] == "Survey (FNDDS)":
            results.append(SearchResult(food))
    return results

# Gets food by fdc id
def _get_food(fdc_id: int):
    endpoint = BASE_URL + FOOD_DETAIL_PATH.format(fdc_id)
    params = {"api_key": API_KEY}
    r = requests.get(endpoint, params=params)
    r.raise_for_status()
    return r.json()
