from flask import Blueprint, request, jsonify
from models import db, Match
from utils.token_utils import token_required

# Viktigt: Se till att variabeln heter exakt "match_routes"
match_routes = Blueprint('match_routes', __name__)


@match_routes.route('/', methods=['GET'])
def get_all_matches():
    """Hämta alla matcher"""
    matches = Match.query.all()
    result = []
    for match in matches:
        result.append({
            'id': match.id,
            'hemmalag_id': match.hemmalag_id,
            'bortalag_id': match.bortalag_id,
            'datum': match.datum,
            'plats': match.plats,
            'resultat_hemma': match.resultat_hemma,
            'resultat_borta': match.resultat_borta
        })
    return jsonify(result), 200


@match_routes.route('/<int:match_id>', methods=['GET'])
def get_match(match_id):
    """Hämta en specifik match baserat på ID"""
    match = Match.query.get_or_404(match_id)
    return jsonify({
        'id': match.id,
        'hemmalag_id': match.hemmalag_id,
        'bortalag_id': match.bortalag_id,
        'datum': match.datum,
        'plats': match.plats,
        'resultat_hemma': match.resultat_hemma,
        'resultat_borta': match.resultat_borta
    }), 200


@match_routes.route('/', methods=['POST'])
@token_required
def create_match():
    """Skapa en ny match"""
    data = request.get_json()

    # Kontrollera att nödvändig data finns
    required_fields = ['hemmalag_id', 'bortalag_id', 'datum', 'plats']
    missing_fields = [field for field in required_fields if field not in data]

    if missing_fields:
        return jsonify({
            'error': f'Följande fält saknas: {", ".join(missing_fields)}'
        }), 400

    # Skapa ny match
    ny_match = Match(
        hemmalag_id=data['hemmalag_id'],
        bortalag_id=data['bortalag_id'],
        datum=data['datum'],
        plats=data['plats'],
        resultat_hemma=data.get('resultat_hemma'),
        resultat_borta=data.get('resultat_borta')
    )

    db.session.add(ny_match)
    db.session.commit()

    return jsonify({
        'message': 'Match skapad',
        'match': {
            'id': ny_match.id,
            'hemmalag_id': ny_match.hemmalag_id,
            'bortalag_id': ny_match.bortalag_id,
            'datum': ny_match.datum,
            'plats': ny_match.plats,
            'resultat_hemma': ny_match.resultat_hemma,
            'resultat_borta': ny_match.resultat_borta
        }
    }), 201


@match_routes.route('/<int:match_id>', methods=['PUT'])
@token_required
def update_match(match_id):
    """Uppdatera en befintlig match"""
    match = Match.query.get_or_404(match_id)
    data = request.get_json()

    # Uppdatera fält om de finns i data
    if 'hemmalag_id' in data:
        match.hemmalag_id = data['hemmalag_id']
    if 'bortalag_id' in data:
        match.bortalag_id = data['bortalag_id']
    if 'datum' in data:
        match.datum = data['datum']
    if 'plats' in data:
        match.plats = data['plats']
    if 'resultat_hemma' in data:
        match.resultat_hemma = data['resultat_hemma']
    if 'resultat_borta' in data:
        match.resultat_borta = data['resultat_borta']

    db.session.commit()

    return jsonify({
        'message': 'Match uppdaterad',
        'match': {
            'id': match.id,
            'hemmalag_id': match.hemmalag_id,
            'bortalag_id': match.bortalag_id,
            'datum': match.datum,
            'plats': match.plats,
            'resultat_hemma': match.resultat_hemma,
            'resultat_borta': match.resultat_borta
        }
    }), 200


@match_routes.route('/<int:match_id>', methods=['DELETE'])
@token_required
def delete_match(match_id):
    """Ta bort en match"""
    match = Match.query.get_or_404(match_id)

    db.session.delete(match)
    db.session.commit()

    return jsonify({'message': f'Match med ID {match_id} har tagits bort'}), 200