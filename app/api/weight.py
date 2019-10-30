from flask import g, jsonify
import json

from app.api import bp
from app.api.auth import basic_auth
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
