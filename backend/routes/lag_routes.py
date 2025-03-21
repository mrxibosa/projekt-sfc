from flask import Blueprint, request, jsonify, current_app
from models import db, Lag, User, user_lag
from decorators import token_required

# Skapa Blueprint
lag_routes = Blueprint('lag_routes', __name__)

# 1. Lägg till en användare till ett lag
@lag_routes.route('/<int:lag_id>/members', methods=['POST'])
@token_required
def add_user_to_lag(current_user, lag_id):
    data = request.get_json()
    user_id = data.get('user_id')
    roll = data.get('roll', 'spelare')
    position = data.get('position')

    # Validera indata
    if not user_id:
        return jsonify({"error": "user_id krävs"}), 400

    lag = Lag.query.get(lag_id)
    user = User.query.get(user_id)

    # Kontrollera att lag och användare existerar
    if not lag or not user:
        return jsonify({"error": "Användare eller lag hittades inte"}), 404

    # Kontrollera om användaren redan är medlem
    association_exists = db.session.query(user_lag).filter_by(user_id=user.id, lag_id=lag.id).first()
    if association_exists:
        return jsonify({"error": "Användaren finns redan i laget"}), 409

    # Lägg till användaren i laget
    db.session.execute(user_lag.insert().values(
        user_id=user.id,
        lag_id=lag.id,
        roll=roll,
        position=position
    ))
    db.session.commit()

    return jsonify({
        "message": f"{user.namn} lades till i laget {lag.namn} som {roll}."
    }), 201

# 2. Hämta alla medlemmar i ett lag
@lag_routes.route('/<int:lag_id>/members', methods=['GET'])
@token_required
def get_lag_members(current_user, lag_id):
    lag = Lag.query.get(lag_id)

    # Kontrollera att laget existerar
    if not lag:
        return jsonify({"error": "Lag hittades inte"}), 404

    # Hämta och serialisera medlemmar
    medlemmar = [medlem.serialize() for medlem in lag.medlemmar]

    return jsonify({
        "lag": lag.namn,
        "medlemmar": medlemmar
    }), 200

# 3. Skapa ett nytt lag
@lag_routes.route('/', methods=['POST'])
@token_required
def create_lag(current_user):
    data = request.get_json()

    if not data or not data.get('namn'):
        return jsonify({"message": "Lagnamn krävs"}), 400

    new_lag = Lag(namn=data.get('namn'))
    db.session.add(new_lag)
    db.session.commit()

    return jsonify({"message": "Lag skapat", "lag": new_lag.serialize()}), 201

# 4. Hämta alla lag
@lag_routes.route('/', methods=['GET'])
@token_required
def get_all_lag(current_user):
    lag_list = Lag.query.all()
    return jsonify({"lag": [lag.serialize() for lag in lag_list]}), 200
