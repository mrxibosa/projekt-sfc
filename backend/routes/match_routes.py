from flask import Blueprint, request, jsonify
from models import db, Match, Lag
from utils.token_utils import token_required, roles_required
from utils.validators import validate_json
from datetime import datetime

# VIKTIGT: Variabeln måste heta exakt "match_routes"
match_routes = Blueprint('match_routes', __name__)


@match_routes.route('/', methods=['GET'])
def get_all_matches():
    """Hämta alla matcher"""
    try:
        matches = Match.query.all()
        result = []

        for match in matches:
            # Hämta lagnamn
            hemmalag = Lag.query.get(match.hemmalag_id)
            bortalag = Lag.query.get(match.bortalag_id)

            result.append({
                'id': match.id,
                'hemmalag_id': match.hemmalag_id,
                'hemmalag_namn': hemmalag.namn if hemmalag else None,
                'bortalag_id': match.bortalag_id,
                'bortalag_namn': bortalag.namn if bortalag else None,
                'datum': match.datum.isoformat() if match.datum else None,
                'plats': match.plats,
                'resultat_hemma': match.resultat_hemma,
                'resultat_borta': match.resultat_borta
            })

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": f"Ett fel inträffade: {str(e)}"}), 500


@match_routes.route('/<int:match_id>', methods=['GET'])
def get_match(match_id):
    """Hämta en specifik match baserat på ID"""
    try:
        match = Match.query.get_or_404(match_id)

        # Hämta lagnamn
        hemmalag = Lag.query.get(match.hemmalag_id)
        bortalag = Lag.query.get(match.bortalag_id)

        return jsonify({
            'id': match.id,
            'hemmalag_id': match.hemmalag_id,
            'hemmalag_namn': hemmalag.namn if hemmalag else None,
            'bortalag_id': match.bortalag_id,
            'bortalag_namn': bortalag.namn if bortalag else None,
            'datum': match.datum.isoformat() if match.datum else None,
            'plats': match.plats,
            'resultat_hemma': match.resultat_hemma,
            'resultat_borta': match.resultat_borta
        }), 200

    except Exception as e:
        return jsonify({"error": f"Ett fel inträffade: {str(e)}"}), 500


@match_routes.route('/', methods=['POST'])
@token_required
@roles_required(['admin', 'tränare'])
@validate_json(['hemmalag_id', 'bortalag_id', 'datum', 'plats'])
def create_match(current_user):
    """Skapa en ny match"""
    try:
        data = request.get_json()

        # Kontrollera att lagen finns
        hemmalag = Lag.query.get(data['hemmalag_id'])
        bortalag = Lag.query.get(data['bortalag_id'])

        if not hemmalag or not bortalag:
            return jsonify({'error': 'Ett eller båda lagen finns inte'}), 400

        # Konvertera datum-sträng till datetime
        try:
            datum = datetime.fromisoformat(data['datum'].replace('Z', '+00:00'))
        except ValueError:
            return jsonify({'error': 'Ogiltigt datumformat, använd ISO 8601 (YYYY-MM-DDTHH:MM:SS)'}), 400

        # Skapa ny match
        ny_match = Match(
            hemmalag_id=data['hemmalag_id'],
            bortalag_id=data['bortalag_id'],
            datum=datum,
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
                'datum': ny_match.datum.isoformat() if ny_match.datum else None,
                'plats': ny_match.plats,
                'resultat_hemma': ny_match.resultat_hemma,
                'resultat_borta': ny_match.resultat_borta
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Ett fel inträffade: {str(e)}"}), 500


@match_routes.route('/<int:match_id>', methods=['PUT'])
@token_required
@roles_required(['admin', 'tränare'])
def update_match(current_user, match_id):
    """Uppdatera en befintlig match"""
    try:
        match = Match.query.get_or_404(match_id)
        data = request.get_json()

        # Uppdatera fält om de finns i data
        if 'hemmalag_id' in data:
            # Kontrollera att laget finns
            if not Lag.query.get(data['hemmalag_id']):
                return jsonify({'error': 'Hemmalaget finns inte'}), 400
            match.hemmalag_id = data['hemmalag_id']

        if 'bortalag_id' in data:
            # Kontrollera att laget finns
            if not Lag.query.get(data['bortalag_id']):
                return jsonify({'error': 'Bortalaget finns inte'}), 400
            match.bortalag_id = data['bortalag_id']

        if 'datum' in data:
            try:
                match.datum = datetime.fromisoformat(data['datum'].replace('Z', '+00:00'))
            except ValueError:
                return jsonify({'error': 'Ogiltigt datumformat, använd ISO 8601 (YYYY-MM-DDTHH:MM:SS)'}), 400

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
                'datum': match.datum.isoformat() if match.datum else None,
                'plats': match.plats,
                'resultat_hemma': match.resultat_hemma,
                'resultat_borta': match.resultat_borta
            }
        }), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Ett fel inträffade: {str(e)}"}), 500


@match_routes.route('/<int:match_id>', methods=['DELETE'])
@token_required
@roles_required(['admin'])
def delete_match(current_user, match_id):
    """Ta bort en match"""
    try:
        match = Match.query.get_or_404(match_id)

        db.session.delete(match)
        db.session.commit()

        return jsonify({'message': f'Match med ID {match_id} har tagits bort'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Ett fel inträffade: {str(e)}"}), 500