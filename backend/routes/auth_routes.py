from flask import Blueprint, request, jsonify
from models import db, User
import jwt
import datetime

auth_routes = Blueprint('auth_routes', __name__)

SECRET_KEY = "superhemlignyckel"


@auth_routes.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        email = data.get('email')
        # Accept both Swedish and English field names
        lösenord = data.get('lösenord') or data.get('password')

        if not email or not lösenord:
            return jsonify({"error": "Both email and password are required"}), 400

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(lösenord):
            return jsonify({"error": "Invalid email or password"}), 401

        # Create token with user_id and role for authorization
        token = jwt.encode(
            {
                'user_id': user.id,
                'roll': user.roll,
                'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
            },
            SECRET_KEY,
            algorithm="HS256"
        )

        return jsonify({
            "message": "Login successful",
            "token": token,
            "user": {
                "id": user.id,
                "namn": user.namn,
                "email": user.email,
                "roll": user.roll
            }
        }), 200

    except Exception as e:
        return jsonify({"error": f"Login failed: {str(e)}"}), 500


@auth_routes.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400

        # Accept both Swedish and English field names
        namn = data.get('namn') or data.get('name')
        email = data.get('email')
        lösenord = data.get('lösenord') or data.get('password')
        roll = data.get('roll') or data.get('role', 'spelare')  # Default to 'spelare' if not provided

        if not namn or not email or not lösenord:
            return jsonify({"error": "Name, email and password are required"}), 400

        user_exists = User.query.filter_by(email=email).first()
        if user_exists:
            return jsonify({"error": "Email already registered"}), 409

        new_user = User(namn=namn, email=email, roll=roll)
        new_user.set_password(lösenord)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": "Registration successful",
            "user": {
                "id": new_user.id,
                "namn": new_user.namn,
                "email": new_user.email,
                "roll": new_user.roll
            }
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500


@auth_routes.route('/me', methods=['GET'])
def get_current_user():
    # Get token from Authorization header
    auth_header = request.headers.get('Authorization')
    if not auth_header or not auth_header.startswith('Bearer '):
        return jsonify({"error": "Authorization token is missing"}), 401

    token = auth_header.split(' ')[1]

    try:
        # Decode token
        data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        user = User.query.get(data['user_id'])

        if not user:
            return jsonify({"error": "User not found"}), 404

        return jsonify({
            "user": {
                "id": user.id,
                "namn": user.namn,
                "email": user.email,
                "roll": user.roll
            }
        }), 200

    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token has expired"}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Invalid token"}), 401
    except Exception as e:
        return jsonify({"error": f"Authentication error: {str(e)}"}), 500