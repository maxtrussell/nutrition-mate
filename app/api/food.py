from flask import g, jsonify, request, Response
import typing as t

from app.api import bp
from app.api.auth import basic_auth
from app.api.errors import error_response, bad_request
import app.model.food as _food
from app.pkg.config import Config
from app.pkg.db import get_db

config = Config()

@bp.route("/api/food", methods=["GET"])
@basic_auth.login_required
def get_all_foods():
    foods = _food.get_all_foods(get_db(config), config.db.FOODS, g.current_user.username)
    foods_json = [food.__dict__ for food in foods]
    return jsonify({"foods": foods_json})

@bp.route("/api/food/<id>", methods=["GET"])
@basic_auth.login_required
def get_food(id: int):
    food = _food.get_food(get_db(config), config.db.FOODS, id, g.current_user.username)
    return jsonify(food.__dict__)

@bp.route("/api/food", methods=["POST"])
@basic_auth.login_required
def post_food():
    data = {}
    if isinstance(request.json, list):
        data["ids"] = []
        for food_dict in request.json:
            data["ids"].append(_add_food(food_dict))
    else:
        data["id"] = _add_food(request.json)
    return jsonify(data)

@bp.route("/api/food", methods=["DELETE"])
@basic_auth.login_required
def delete_food():
    ids = request.json.get("ids")
    for food_id in ids:
        _food.delete_by_id(get_db(config), config.db.FOODS, food_id, g.current_user.username)
    return jsonify({"success": True})

def _add_food(data: t.Dict):
    try:
        new_food = _food.Food(
            name=data['name'],
            calories=data.get('calories'),
            servings=data.get('servings', {}),
            fat=data.get('fat', 0.0),
            carbs=data.get('carbs', 0.0),
            protein=data.get('protein', 0.0),
            alcohol=data.get('alcohol', 0.0),
            sugar=data.get('sugar', 0.0),
            fiber=data.get('fiber', 0.0),
            user=g.current_user.username,
        )
        new_food = new_food.normalize(data.get('quantity', 100))
        food_id = new_food.insert(get_db(config), config.db.FOODS)
        return food_id
    except KeyError as e:
        return bad_request("'name' and 'quantity' are required.")
    except Exception as e:
        return error_response(500)

