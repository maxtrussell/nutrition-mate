from datetime import datetime
from flask import g, jsonify, request, Response

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
    dt = request.json.get('date')
    weight = request.json.get('weight')
    notes = request.json.get('notes', '')
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
        return Response('', status=201, mimetype='application/json')
    except ValueError as e:
        return bad_request(str(e))
    except Exception as e:
        return error_response(500)
