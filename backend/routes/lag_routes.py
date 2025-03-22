from flask import Blueprint, request, jsonify
from models import db, Lag, User, user_lag
from decorators import token_required, roles_required
from utils.validators import validate_json
import logging

lag_routes = Blueprint('lag_routes', __name__)
logger = logging.getLogger(__name__)

ADMIN_ROLES = ['admin', 'superadmin']
COACH_ROLES = ['tränare', 'admin', 'superadmin']


@lag_routes.route('/', methods=['POST'])
@token_required
@roles_required(ADMIN_ROLES)
@validate_json(['namn'])
def create_lag(current_user):
    data = request.get_json()

    if Lag.query.filter_by(namn=data['namn']).first():
        return jsonify({"error": f"Team {data['namn']} already exists"}), 409

    new_team = Lag(namn=data['namn'])
    db.session.add(new_team)
    db.session.commit()

    if data.get('add_creator', True):
        db.session.execute(user_lag.insert().values(
            user_id=current_user.id,
            lag_id=new_team.id,
            roll='tränare',
            position=data.get('position', 'head coach')
        ))
        db.session.commit()

    logger.info(f"Team created: {new_team.namn} by user {current_user.id}")
    return jsonify({"message": "Team created", "team": new_team.serialize()}), 201


@lag_routes.route('/', methods=['GET'])
@token_required
def get_all_lag(current_user):
    try:
        query = Lag.query
        search = request.args.get('search')
        if search:
            query = query.filter(Lag.namn.ilike(f"%{search}%"))

        sort_by = request.args.get('sort_by', 'namn')
        sort_order = request.args.get('sort_order', 'asc')

        if sort_order.lower() == 'desc':
            query = query.order_by(getattr(Lag, sort_by).desc())
        else:
            query = query.order_by(getattr(Lag, sort_by).asc())

        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)

        pagination = query.paginate(page=page, per_page=per_page)
        teams = pagination.items

        return jsonify({
            "teams": [team.serialize() for team in teams],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving teams: {str(e)}")
        return jsonify({"error": str(e)}), 500


@lag_routes.route('/<int:lag_id>', methods=['GET'])
@token_required
def get_lag(current_user, lag_id):
    team = Lag.query.get_or_404(lag_id)
    if request.args.get('include_members', 'false').lower() == 'true':
        return jsonify({"team": team.serialize_with_members()}), 200
    return jsonify({"team": team.serialize()}), 200


@lag_routes.route('/<int:lag_id>', methods=['PUT'])
@token_required
@roles_required(ADMIN_ROLES)
@validate_json(['namn'])
def update_lag(current_user, lag_id):
    team = Lag.query.get_or_404(lag_id)
    data = request.get_json()

    if Lag.query.filter(Lag.namn == data['namn'], Lag.id != lag_id).first():
        return jsonify({"error": f"Team name '{data['namn']}' already in use"}), 409

    team.namn = data['namn']
    db.session.commit()

    logger.info(f"Team updated: {team.id}")
    return jsonify({"message": "Team updated", "team": team.serialize()}), 200


@lag_routes.route('/<int:lag_id>', methods=['DELETE'])
@token_required
@roles_required(ADMIN_ROLES)
def delete_lag(current_user, lag_id):
    team = Lag.query.get_or_404(lag_id)
    db.session.delete(team)
    db.session.commit()
    logger.info(f"Team deleted: {team.id}")
    return jsonify({"message": "Team deleted"}), 200


@lag_routes.route('/<int:lag_id>/users', methods=['POST'])
@token_required
@roles_required(COACH_ROLES)
@validate_json(['user_id', 'roll'])
def add_user_to_lag(current_user, lag_id):
    Lag.query.get_or_404(lag_id)
    data = request.get_json()

    if not User.query.get(data['user_id']):
        return jsonify({"error": "User not found"}), 404

    if db.session.query(user_lag).filter_by(user_id=data['user_id'], lag_id=lag_id).first():
        return jsonify({"error": "User already in team"}), 409

    db.session.execute(user_lag.insert().values(
        user_id=data['user_id'],
        lag_id=lag_id,
        roll=data['roll'],
        position=data.get('position')
    ))
    db.session.commit()

    return jsonify({"message": "User added to team"}), 201


@lag_routes.route('/<int:lag_id>/users/<int:user_id>', methods=['DELETE'])
@token_required
@roles_required(COACH_ROLES)
def remove_user_from_lag(current_user, lag_id, user_id):
    Lag.query.get_or_404(lag_id)
    User.query.get_or_404(user_id)
    deleted = db.session.query(user_lag).filter_by(user_id=user_id, lag_id=lag_id).delete()
    if not deleted:
        return jsonify({"error": "User not in team"}), 404
    db.session.commit()
    return jsonify({"message": "User removed from team"}), 200


@lag_routes.route('/<int:lag_id>/users', methods=['GET'])
@token_required
def get_lag_users(current_user, lag_id):
    Lag.query.get_or_404(lag_id)
    users = db.session.query(User, user_lag.c.roll, user_lag.c.position).join(
        user_lag, User.id == user_lag.c.user_id).filter(user_lag.c.lag_id == lag_id).all()

    result = [{
        "id": user.id,
        "namn": user.namn,
        "email": user.email,
        "roll": roll,
        "position": position
    } for user, roll, position in users]

    return jsonify({"team_id": lag_id, "users": result}), 200


@lag_routes.route('/<int:lag_id>/users/<int:user_id>', methods=['PUT'])
@token_required
@roles_required(COACH_ROLES)
def update_user_team_role(current_user, lag_id, user_id):
    data = request.get_json()

    Lag.query.get_or_404(lag_id)
    User.query.get_or_404(user_id)
    if not db.session.query(user_lag).filter_by(user_id=user_id, lag_id=lag_id).first():
        return jsonify({"error": "User not in team"}), 404

    updates = {}
    if 'roll' in data:
        updates['roll'] = data['roll']
    if 'position' in data:
        updates['position'] = data['position']

    if not updates:
        return jsonify({"error": "No updates provided"}), 400

    db.session.query(user_lag).filter_by(user_id=user_id, lag_id=lag_id).update(updates)
    db.session.commit()

    return jsonify({"message": "User's role updated"}), 200