from flask import Blueprint, jsonify, request
from models import db, User
from decorators import token_required, roles_required
from utils.validators import validate_json
import logging

user_routes = Blueprint('user_routes', __name__)
logger = logging.getLogger(__name__)

# 🟢 Hämta info om inloggad användare
@user_routes.route('/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    logger.info(f"Användare {current_user.id} hämtade sina uppgifter.")
    return jsonify(current_user.serialize()), 200


# 🟢 Skapa en ny användare (Endast admin)
@user_routes.route('/', methods=['POST'])
@token_required
@roles_required(['admin'])
@validate_json(['namn', 'email', 'lösenord', 'roll'])
def create_user(current_user):
    data = request.get_json()

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"error": "E-postadressen är redan registrerad"}), 409

    new_user = User(
        namn=data['namn'],
        email=data['email'],
        roll=data['roll']
    )
    new_user.set_password(data['lösenord'])
    db.session.add(new_user)
    db.session.commit()

    logger.info(f"Admin {current_user.id} skapade användare {data['email']}")
    return jsonify({"message": "Användare skapad", "user": new_user.serialize()}), 201


# 📄 Hämta alla användare (Endast admin)
@user_routes.route('/', methods=['GET'])
@token_required
@roles_required(['admin'])
def get_all_users(current_user):
    users = User.query.all()
    logger.info(f"Admin {current_user.id} hämtade alla användare.")
    return jsonify({"users": [user.serialize() for user in users]}), 200


# 📄 Hämta en specifik användare (Endast admin)
@user_routes.route('/<int:user_id>', methods=['GET'])
@token_required
@roles_required(['admin'])
def get_user_by_id(current_user, user_id):
    user = User.query.get_or_404(user_id)
    logger.info(f"Admin {current_user.id} hämtade användare {user_id}.")
    return jsonify({"user": user.serialize()}), 200


# 🛠 Uppdatera info om användare (Endast admin)
@user_routes.route('/<int:user_id>', methods=['PUT'])
@token_required
@roles_required(['admin'])
@validate_json(['namn', 'email', 'roll'])
def update_user(current_user, user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json()

    user.namn = data['namn']
    user.email = data['email']
    user.roll = data['roll']
    db.session.commit()

    logger.info(f"Admin {current_user.id} uppdaterade användare {user_id}.")
    return jsonify({"message": "Användare uppdaterad", "user": user.serialize()}), 200


# 🔒 Uppdatera lösenord (Admin eller användaren själv)
@user_routes.route('/<int:user_id>/password', methods=['PUT'])
@token_required
@validate_json(['lösenord'])
def update_password(current_user, user_id):
    user = User.query.get_or_404(user_id)
    if current_user.id != user.id and current_user.roll != "admin":
        return jsonify({"error": "Endast användaren själv eller admin kan ändra lösenord"}), 403

    data = request.get_json()
    user.set_password(data['lösenord'])
    db.session.commit()

    logger.info(f"Lösenord ändrat för användare {user_id} av {current_user.id}.")
    return jsonify({"message": "Lösenord uppdaterat"}), 200


# 🗑 Ta bort en användare (Endast admin)
@user_routes.route('/<int:user_id>', methods=['DELETE'])
@token_required
@roles_required(['admin'])
def delete_user(current_user, user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    logger.info(f"Admin {current_user.id} tog bort användare {user_id}.")
    return jsonify({"message": "Användare borttagen"}), 200
