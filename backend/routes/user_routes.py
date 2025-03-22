from flask import Blueprint, jsonify, request
from models import db, User
from decorators import token_required
import logging

# Skapa Blueprint
user_routes = Blueprint('user_routes', __name__)

# 🛠 Hjälpfunktion: Validera inkommande data
def validate_request_data(required_fields):
    data = request.get_json()
    if not data:
        return None, jsonify({"error": "Ingen data skickades"}), 400
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return None, jsonify({"error": f"Saknar följande fält: {', '.join(missing_fields)}"}), 400
    return data, None

# 🛠 Hjälpfunktion: Loggning
logging.basicConfig(level=logging.INFO)


# 🟢 Hämta info om inloggad användare
@user_routes.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    logging.info(f"Användare {current_user.id} hämtade sina uppgifter.")
    return jsonify({
        "id": current_user.id,
        "namn": current_user.namn,
        "email": current_user.email,
        "roll": current_user.roll
    }), 200


# 🟢 Skapa en ny användare (Endast admin)
@user_routes.route('/', methods=['POST'])
@token_required
def create_user(current_user):
    if current_user.roll != "admin":
        return jsonify({"error": "Endast admin kan skapa nya användare"}), 403

    data, error = validate_request_data(['namn', 'email', 'lösenord', 'roll'])
    if error:
        return error

    user_exists = User.query.filter_by(email=data['email']).first()
    if user_exists:
        return jsonify({"error": "E-postadressen är redan registrerad"}), 409

    new_user = User(
        namn=data['namn'],
        email=data['email'],
        roll=data['roll']
    )
    new_user.set_password(data['lösenord'])
    db.session.add(new_user)
    db.session.commit()

    logging.info(f"Admin {current_user.id} skapade en ny användare med e-post: {data['email']}.")
    return jsonify({"message": "Användare skapad", "user": new_user.serialize()}), 201


# 📄 Hämta alla användare (Endast admin)
@user_routes.route('/', methods=['GET'])
@token_required
def get_all_users(current_user):
    if current_user.roll != "admin":
        return jsonify({"error": "Endast admin kan hämta alla användare"}), 403

    users = User.query.all()
    logging.info(f"Admin {current_user.id} hämtade alla användare.")
    return jsonify({"users": [user.serialize() for user in users]}), 200


# 📄 Hämta en specifik användare (Endast admin)
@user_routes.route('/<int:user_id>', methods=['GET'])
@token_required
def get_user_by_id(current_user, user_id):
    if current_user.roll != "admin":
        return jsonify({"error": "Endast admin kan hämta användardetaljer"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Användare hittades inte"}), 404

    logging.info(f"Admin {current_user.id} hämtade användardetaljer för användare {user_id}.")
    return jsonify({"user": user.serialize()}), 200


# 🛠 Uppdatera info om en användare (Endast admin)
@user_routes.route('/<int:user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    if current_user.roll != "admin":
        return jsonify({"error": "Endast admin kan uppdatera användare"}), 403

    data, error = validate_request_data(['namn', 'email', 'roll'])
    if error:
        return error

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Användare hittades inte"}), 404

    user.namn = data['namn']
    user.email = data['email']
    user.roll = data['roll']
    db.session.commit()

    logging.info(f"Admin {current_user.id} uppdaterade användare {user_id}.")
    return jsonify({"message": "Användare uppdaterad", "user": user.serialize()}), 200


# 🔒 Uppdatera lösenord för en användare (Endast inloggad användare eller admin)
@user_routes.route('/<int:user_id>/password', methods=['PUT'])
@token_required
def update_password(current_user, user_id):
    data, error = validate_request_data(['lösenord'])
    if error:
        return error

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Användare hittades inte"}), 404

    # Endast användaren själv eller admin kan uppdatera lösenord
    if current_user.id != user.id and current_user.roll != "admin":
        return jsonify({"error": "Endast användaren själv eller admin kan uppdatera lösenord"}), 403

    user.set_password(data['lösenord'])
    db.session.commit()

    logging.info(f"Användare {current_user.id} uppdaterade lösenord för användare {user_id}.")
    return jsonify({"message": "Lösenord uppdaterat"}), 200


# 🗑 Ta bort en användare (Endast admin)
@user_routes.route('/<int:user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user, user_id):
    if current_user.roll != "admin":
        return jsonify({"error": "Endast admin kan ta bort användare"}), 403

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "Användare hittades inte"}), 404

    db.session.delete(user)
    db.session.commit()

    logging.info(f"Admin {current_user.id} tog bort användare {user_id}.")
    return jsonify({"message": "Användare borttagen"}), 200
