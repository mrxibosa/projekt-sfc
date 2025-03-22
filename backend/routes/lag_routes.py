from flask import Blueprint, request, jsonify
from models import db, Lag
from utils.token_utils import token_required

# Detta är det viktiga - se till att variabeln heter exakt "lag_routes"
lag_routes = Blueprint('lag_routes', __name__)


@lag_routes.route('/', methods=['GET'])
def get_all_lag():
    """Hämta alla lag"""
    lag = Lag.query.all()
    result = []
    for l in lag:
        result.append({
            'id': l.id,
            'namn': l.namn,
            'beskrivning': l.beskrivning
        })
    return jsonify(result), 200


@lag_routes.route('/<int:lag_id>', methods=['GET'])
def get_lag(lag_id):
    """Hämta ett specifikt lag baserat på ID"""
    lag = Lag.query.get_or_404(lag_id)
    return jsonify({
        'id': lag.id,
        'namn': lag.namn,
        'beskrivning': lag.beskrivning
    }), 200


@lag_routes.route('/', methods=['POST'])
@token_required
def create_lag():
    """Skapa ett nytt lag"""
    data = request.get_json()

    # Kontrollera att nödvändig data finns
    if not data or 'namn' not in data:
        return jsonify({'error': 'Namn är obligatoriskt'}), 400

    # Skapa nytt lag
    nytt_lag = Lag(
        namn=data['namn'],
        beskrivning=data.get('beskrivning', '')
    )

    db.session.add(nytt_lag)
    db.session.commit()

    return jsonify({
        'message': 'Lag skapat',
        'lag': {
            'id': nytt_lag.id,
            'namn': nytt_lag.namn,
            'beskrivning': nytt_lag.beskrivning
        }
    }), 201


@lag_routes.route('/<int:lag_id>', methods=['PUT'])
@token_required
def update_lag(lag_id):
    """Uppdatera ett befintligt lag"""
    lag = Lag.query.get_or_404(lag_id)
    data = request.get_json()

    if 'namn' in data:
        lag.namn = data['namn']
    if 'beskrivning' in data:
        lag.beskrivning = data['beskrivning']

    db.session.commit()

    return jsonify({
        'message': 'Lag uppdaterat',
        'lag': {
            'id': lag.id,
            'namn': lag.namn,
            'beskrivning': lag.beskrivning
        }
    }), 200


@lag_routes.route('/<int:lag_id>', methods=['DELETE'])
@token_required
def delete_lag(lag_id):
    """Ta bort ett lag"""
    lag = Lag.query.get_or_404(lag_id)

    db.session.delete(lag)
    db.session.commit()

    return jsonify({'message': f'Lag med ID {lag_id} har tagits bort'}), 200