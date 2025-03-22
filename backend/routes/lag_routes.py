from flask import Blueprint, request, jsonify
from models import db, Lag, user_lag
from decorators import token_required
import logging

# Initialisera Blueprint
lag_routes = Blueprint('lag_routes', __name__)

# 🛠 Hjälpfunktion: Kontrollera roll
def has_role(current_user, roll, lag_id=None):
    if roll == "admin":
        return current_user.roll == "admin"
    elif roll == "tränare" and lag_id:
        user_lag_entry = db.session.query(user_lag).filter_by(user_id=current_user.id, lag_id=lag_id).first()
        return user_lag_entry and user_lag_entry.roll == "tränare"
    return False

# 🛠 Hjälpfunktion: Validera inkommande data
def validate_request_data(required_fields):
    data = request.get_json()
    if not data:
        return None, jsonify({"error": "Ingen data skickades"}), 400
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return None, jsonify({"error": f"Saknar följande fält: {', '.join(missing_fields)}"}), 400
    return data, None


### 🟢 CREATE: Skapa ett nytt lag (Endast admin)
@lag_routes.route('/', methods=['POST'])
@token_required
def create_lag(current_user):
    data, error = validate_request_data(['namn'])
    if error:
        return error

    # Endast admin kan skapa lag
    if not has_role(current_user, "admin"):
        return jsonify({"error": "Endast admin kan skapa lag"}), 403

    new_lag = Lag(namn=data['namn'])
    db.session.add(new_lag)
    db.session.commit()

    logging.info(f"Admin {current_user.id} skapade laget: {new_lag.namn}")
    return jsonify({"message": "Lag skapat", "lag": new_lag.serialize()}), 201


### 📄 READ: Hämta alla lag där användaren är medlem
@lag_routes.route('/', methods=['GET'])
@token_required
def get_all_lag(current_user):
    lag_list = Lag.query.join(user_lag).filter(user_lag.c.user_id == current_user.id).all()
    logging.info(f"Användare {current_user.id} hämtade sina lag.")
    return jsonify({"lag": [lag.serialize() for lag in lag_list]}), 200


### 📄 READ: Hämta detaljer om ett specifikt lag
@lag_routes.route('/<int:lag_id>', methods=['GET'])
@token_required
def get_lag(current_user, lag_id):
    lag = Lag.query.get(lag_id)
    if not lag:
        return jsonify({"error": "Lag hittades inte"}), 404

    logging.info(f"Användare {current_user.id} hämtade detaljer för lag {lag_id}.")
    return jsonify({"lag": lag.serialize()}), 200


### 📄 READ: Hämta medlemmar i ett lag
@lag_routes.route('/<int:lag_id>/members', methods=['GET'])
@token_required
def get_lag_members(current_user, lag_id):
    lag = Lag.query.get(lag_id)
    if not lag:
        return jsonify({"error": "Lag hittades inte"}), 404

    # Endast tränare och lagmedlemmar kan se medlemmarna
    if not has_role(current_user, "tränare", lag_id):
        return jsonify({"error": "Du har inte behörighet att se medlemmar i detta lag"}), 403

    medlemmar = [user.serialize() for user in lag.medlemmar]
    logging.info(f"Användare {current_user.id} hämtade medlemmar för lag {lag_id}.")
    return jsonify({"lag": lag.namn, "medlemmar": medlemmar}), 200


### 🛠 UPDATE: Lägg till en medlem i ett lag (Endast tränare)
@lag_routes.route('/<int:lag_id>/members', methods=['POST'])
@token_required
def add_user_to_lag(current_user, lag_id):
    data, error = validate_request_data(['user_id', 'roll', 'position'])
    if error:
        return error

    lag = Lag.query.get(lag_id)
    if not lag:
        return jsonify({"error": "Lag hittades inte"}), 404

    # Endast tränare kan lägga till medlemmar
    if not has_role(current_user, "tränare", lag_id):
        return jsonify({"error": "Endast tränare kan lägga till medlemmar"}), 403

    exists = db.session.query(user_lag).filter_by(user_id=data['user_id'], lag_id=lag_id).first()
    if exists:
        return jsonify({"error": "Användaren finns redan i laget"}), 409

    db.session.execute(user_lag.insert().values(
        user_id=data['user_id'], lag_id=lag_id, roll=data['roll'], position=data['position']))
    db.session.commit()

    logging.info(f"Tränare {current_user.id} lade till användare {data['user_id']} i lag {lag_id}.")
    return jsonify({"message": f"Användaren har lagts till i laget {lag.namn} som {data['roll']}."}), 201


### 🛠 UPDATE: Uppdatera ett lag (Endast tränare)
@lag_routes.route('/<int:lag_id>', methods=['PUT'])
@token_required
def update_lag(current_user, lag_id):
    data, error = validate_request_data(['namn'])
    if error:
        return error

    lag = Lag.query.get(lag_id)
    if not lag:
        return jsonify({"error": "Lag hittades inte"}), 404

    # Endast tränare kan uppdatera lag
    if not has_role(current_user, "tränare", lag_id):
        return jsonify({"error": "Endast tränare kan uppdatera lag"}), 403

    lag.namn = data['namn']
    db.session.commit()

    logging.info(f"Tränare {current_user.id} uppdaterade lag {lag_id}.")
    return jsonify({"message": "Lag uppdaterat", "lag": lag.serialize()}), 200


### 🗑 DELETE: Ta bort en medlem från ett lag (Endast tränare)
@lag_routes.route('/<int:lag_id>/members/<int:user_id>', methods=['DELETE'])
@token_required
def remove_user_from_lag(current_user, lag_id, user_id):
    lag = Lag.query.get(lag_id)
    if not lag:
        return jsonify({"error": "Lag hittades inte"}), 404

    exists = db.session.query(user_lag).filter_by(user_id=user_id, lag_id=lag_id).first()
    if not exists:
        return jsonify({"error": "Användaren är inte medlem i laget"}), 404

    if not has_role(current_user, "tränare", lag_id):
        return jsonify({"error": "Endast tränare kan ta bort medlemmar"}), 403

    db.session.query(user_lag).filter_by(user_id=user_id, lag_id=lag_id).delete()
    db.session.commit()

    logging.info(f"Tränare {current_user.id} tog bort användare {user_id} från lag {lag_id}.")
    return jsonify({"message": "Medlem borttagen från laget"}), 200


### 🗑 DELETE: Ta bort ett lag (Endast admin)
@lag_routes.route('/<int:lag_id>', methods=['DELETE'])
@token_required
def delete_lag(current_user, lag_id):
    lag = Lag.query.get(lag_id)
    if not lag:
        return jsonify({"error": "Lag hittades inte"}), 404

    if not has_role(current_user, "admin"):
        return jsonify({"error": "Endast admin kan ta bort lag"}), 403

    db.session.delete(lag)
    db.session.commit()

    logging.info(f"Admin {current_user.id} tog bort lag {lag_id}.")
    return jsonify({"message": f"Laget {lag.namn} har tagits bort"}), 200
