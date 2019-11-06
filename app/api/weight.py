from datetime import datetime
from flask import g, jsonify, request, Response
import typing as t

from app.api import bp
from app.api.auth import basic_auth
from app.api.errors import error_response, bad_request
import app.model.weight as _weight
from app.pkg.config import Config
from app.pkg.db import get_db

config = Config()

@bp.route('/api/weight', methods=['GET'])
@basic_auth.login_required
def get_weight():
    user = g.current_user
    weights = _weight.get_last_weights(
        get_db(config), config.db.WEIGHTS, username=user.username
    )

    # Convert data to json format
    data = {}
    for weight in weights:
        data[weight.date] = weight.weight
    return jsonify(data)

@bp.route('/api/weight', methods=['POST'])
@basic_auth.login_required
def post_weight():
    # TODO: return URI to new weight
    if isinstance(request.json, list):
        for weight_dict in request.json:
            _add_weight(weight_dict)
    else:
        _add_weight(request.json)
    return jsonify({"success": True})

def _add_weight(data: t.Dict):
    dt = data.get('date')
    weight = data.get('weight')
    notes = data.get('notes', '')
    if not dt:
        return bad_request('date is a required field.')
    if not weight:
        return bad_request('weight is a required field.')
    try:
        w = _weight.Weight(float(weight))
        w.date = datetime.strptime(dt, "%Y-%m-%d")
        w.notes = notes
        w.username = g.current_user.username
        w.insert(get_db(config), config.db.WEIGHTS)
    except ValueError as e:
        return bad_request(str(e))
    except Exception as e:
        return error_response(500)
