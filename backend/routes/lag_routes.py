from flask import Blueprint, jsonify, request, current_app
from models import Lag, db

lag_routes = Blueprint('lag_routes', __name__)

@lag_routes.route('/', methods=['GET'])
def get_lag():
    try:
        lag_lista = Lag.query.all()
        return jsonify([l.serialize() for l in lag_lista]), 200
    except Exception as e:
        current_app.logger.error("Fel vid hämtning av lag: %s", e)
        return jsonify({"error": str(e)}), 500

@lag_routes.route('/<int:id>', methods=['GET'])
def get_lag_by_id(id):
    try:
        lag_obj = Lag.query.get_or_404(id)
        return jsonify(lag_obj.serialize()), 200
    except Exception as e:
        current_app.logger.error("Fel vid hämtning av lag med id %s: %s", id, e)
        return jsonify({"error": str(e)}), 500
