from flask import Blueprint, request, jsonify
from models import db, User
import jwt
import datetime

auth_routes = Blueprint('auth_routes', __name__)

SECRET_KEY = "superhemlignyckel"

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get('email')
    lösenord = data.get('lösenord')

    user = User.query.filter_by(email=email).first()
    if not user or not user.check_password(lösenord):
        return jsonify({"error": "Ogiltig inloggning"}), 401

    token = jwt.encode({'user_id': user.id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1)},
                       SECRET_KEY, algorithm="HS256")

    return jsonify({"message": "Inloggad", "token": token}), 200

@auth_routes.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    namn = data.get('namn')
    email = data.get('email')
    lösenord = data.get('lösenord')

    if not namn or not email or not lösenord:
        return jsonify({"error": "Alla fält krävs"}), 400

    user_exists = User.query.filter_by(email=email).first()
    if user_exists:
        return jsonify({"error": "E-postadressen är redan registrerad"}), 409

    new_user = User(namn=namn, email=email)
    new_user.set_password(lösenord)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registreringen lyckades"}), 201
