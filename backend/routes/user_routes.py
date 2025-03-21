from flask import Blueprint, jsonify, request, current_app
from models import User, db
from decorators import token_required

user_routes = Blueprint('user_routes', __name__)

@user_routes.route('/', methods=['POST'])
def skapa_anvandare():
    data = request.get_json()
    if not data or not all(key in data for key in ['namn', 'email', 'lösenord']):
        return jsonify({"error": "namn, email och lösenord krävs"}), 400

    try:
        new_user = User(namn=data['namn'], email=data['email'])
        new_user.set_password(data['lösenord'])  # Hash lösenordet
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

@user_routes.route('/', methods=['GET'])
@token_required
def get_users(current_user):
    try:
        users = User.query.all()
        return jsonify([user.serialize() for user in users]), 200
    except Exception as e:
        current_app.logger.error("Fel vid hämtning av användare: %s", e)
        return jsonify({"error": str(e)}), 500
