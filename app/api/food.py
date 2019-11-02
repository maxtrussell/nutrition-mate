from flask import g, jsonify, request, Response
import typing as t

from app.api import bp
from app.api.auth import basic_auth
from app.api.errors import error_response, bad_request
import app.model.food as _food
from app.pkg.config import Config
from app.pkg.db import get_db

config = Config()

@bp.route("/api/food/<id>", methods=["GET"])
@basic_auth.login_required
def get_food(id: int):
    # TODO
    pass

@bp.route("/api/food", methods=["POST"])
@basic_auth.login_required
def post_food():
    # TODO: return uri to new food
    if isinstance(request.json, list):
        for food_dict in request.json:
            _add_food(food_dict)
    else:
        _add_food(request.json)
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
        new_food = new_food.normalize(data['quantity'])
        new_food.insert(get_db(config), config.db.FOODS)
    except KeyError as e:
        return bad_request("'name' and 'quantity' are required.")
    except Exception as e:
        return error_response(500)
