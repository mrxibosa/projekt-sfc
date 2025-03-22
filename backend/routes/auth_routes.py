from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import check_password_hash
import jwt
import datetime
from config import Config
from utils.validators import validate_json

auth_routes = Blueprint('auth_routes', __name__)

@auth_routes.route('/login', methods=['POST'])
@validate_json(['email', 'lösenord'])  # Korrigerat till lösenord med ö för att matcha modellen
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()
        # Kontrollera att användaren finns och att lösenordet stämmer
        if not user or not check_password_hash(user.lösenord_hash, data.get('lösenord')):
            return jsonify({"error": "Invalid credentials"}), 401

        # Skapa JWT-token och avkoda om det returneras som bytes
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, Config.SECRET_KEY, algorithm="HS256")
        if isinstance(token, bytes):
            token = token.decode('utf-8')

        return jsonify({"token": token, "role": user.roll}), 200

    except Exception as e:
        # Logga gärna felet här om du vill
        return jsonify({"error": f"An error occurred during login: {str(e)}"}), 500