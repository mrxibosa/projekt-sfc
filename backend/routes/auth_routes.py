from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import check_password_hash
from utils.validators import validate_json
import jwt
import datetime
from config import Config

# Create blueprint
auth_routes = Blueprint('auth_routes', __name__)

# ========== Register Route ==========

@auth_routes.route('/register', methods=['POST'])
@validate_json(['namn', 'email', 'losenord', 'roll'])
def register():
    try:
        data = request.get_json()

        existing_user = User.query.filter_by(email=data['email']).first()
        if existing_user:
            return jsonify({"error": "Email already registered"}), 400

        new_user = User(
            namn=data['namn'],
            email=data['email'],
            roll=data['roll']
        )
        new_user.set_password(data['losenord'])
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "User registered successfully"}), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"An error occurred during registration: {str(e)}"}), 500


# ========== Login Route ==========

@auth_routes.route('/login', methods=['POST'])
@validate_json(['email', 'losenord'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if not user or not check_password_hash(user.losenord, data['losenord']):
            return jsonify({"error": "Invalid credentials"}), 401

        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, Config.SECRET_KEY, algorithm="HS256")

        return jsonify({"token": token, "role": user.roll}), 200

    except Exception as e:
        return jsonify({"error": f"An error occurred during login: {str(e)}"}), 500
