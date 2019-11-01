from flask import g, jsonify, request, Response

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
    try:
        new_food = _food.Food(
            name=request.json['name'],
            calories=request.json.get('calories'),
            servings=request.json.get('servings', {}),
            fat=request.json.get('fat', 0.0),
            carbs=request.json.get('carbs', 0.0),
            protein=request.json.get('protein', 0.0),
            alcohol=request.json.get('alcohol', 0.0),
            sugar=request.json.get('sugar', 0.0),
            fiber=request.json.get('fiber', 0.0),
            user=g.current_user.username,
        )
        new_food = new_food.normalize(request.json['quantity'])
        new_food.insert(get_db(config), config.db.FOODS)
    except KeyError as e:
        return bad_request("'name' and 'quantity' are required.")
    except Exception as e:
        return error_response(500)
    return jsonify({"success": True})


