from flask import Blueprint, jsonify, request
from models import User
import jwt
import datetime
import os

auth_routes = Blueprint('auth_routes', __name__)

SECRET_KEY = os.getenv("SECRET_KEY", "superhemlignyckel")

@auth_routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data or 'email' not in data or 'lösenord' not in data:
        return jsonify({"error": "Email och lösenord krävs"}), 400

    user = User.query.filter_by(email=data['email']).first()

    if user and user.check_password(data['lösenord']):
        token_payload = {
            "user_id": user.id,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(token_payload, SECRET_KEY, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode('utf-8')
        return jsonify({"message": "Inloggad", "token": token}), 200
    else:
        return jsonify({"error": "Fel email eller lösenord"}), 401
