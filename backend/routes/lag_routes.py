from flask import Blueprint, request, jsonify
from models import db, Lag, User, user_lag
from decorators import token_required, roles_required
import logging

# Create blueprint
lag_routes = Blueprint('lag_routes', __name__)

# Set up logging
logger = logging.getLogger(__name__)

# Define role hierarchies for cleaner permission management
# This allows for more scalable role definitions
ADMIN_ROLES = ['admin', 'superadmin']
COACH_ROLES = ['tränare', 'admin', 'superadmin']
PLAYER_ROLES = ['spelare', 'tränare', 'admin', 'superadmin']
ALL_ROLES = ['gäst', 'spelare', 'tränare', 'admin', 'superadmin']


# ========== Team Routes ==========

@lag_routes.route('/', methods=['POST'])
@token_required
@roles_required(ADMIN_ROLES)
def create_lag(current_user):
    """Create a new team"""
    try:
        data = request.get_json()

        # Validate required fields
        if 'namn' not in data:
            return jsonify({"error": "Team name is required"}), 400

        # Check if team already exists
        existing_team = Lag.query.filter_by(namn=data['namn']).first()
        if existing_team:
            return jsonify({"error": f"Team {data['namn']} already exists"}), 409

        # Create new team
        new_team = Lag(namn=data['namn'])
        db.session.add(new_team)
        db.session.commit()

        # Add the creator as a team member with coach role if specified
        if data.get('add_creator', True):
            team_role = user_lag.insert().values(
                user_id=current_user.id,
                lag_id=new_team.id,
                roll='tränare',
                position=data.get('position', 'head coach')
            )
            db.session.execute(team_role)
            db.session.commit()

        logger.info(f"Team created: {new_team.namn} (id: {new_team.id}) by user {current_user.id}")
        return jsonify({
            "message": "Team created successfully",
            "team": new_team.serialize()
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating team: {str(e)}")
        return jsonify({"error": f"Failed to create team: {str(e)}"}), 500


@lag_routes.route('/', methods=['GET'])
@token_required
def get_all_lag(current_user):
    """Get all teams with optional filtering"""
    try:
        # Define base query
        query = Lag.query

        # Apply search filter if provided
        search = request.args.get('search')
        if search:
            query = query.filter(Lag.namn.ilike(f'%{search}%'))

        # Apply sorting
        sort_by = request.args.get('sort_by', 'namn')
        sort_order = request.args.get('sort_order', 'asc')

        if sort_by not in ['namn', 'id', 'skapad_datum']:
            sort_by = 'namn'  # Default sort

        if sort_order.lower() == 'desc':
            query = query.order_by(getattr(Lag, sort_by).desc())
        else:
            query = query.order_by(getattr(Lag, sort_by).asc())

        # Apply pagination
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
        return jsonify({"error": f"Failed to retrieve teams: {str(e)}"}), 500


@lag_routes.route('/<int:lag_id>', methods=['GET'])
@token_required
def get_lag(current_user, lag_id):
    """Get a specific team by ID with option to include members"""
    try:
        team = Lag.query.get_or_404(lag_id)

        # Check if we should include team members
        include_members = request.args.get('include_members', 'false').lower() == 'true'

        if include_members:
            return jsonify({"team": team.serialize_with_members()}), 200
        else:
            return jsonify({"team": team.serialize()}), 200

    except Exception as e:
        logger.error(f"Error retrieving team {lag_id}: {str(e)}")
        return jsonify({"error": f"Failed to retrieve team: {str(e)}"}), 500


@lag_routes.route('/<int:lag_id>', methods=['PUT'])
@token_required
@roles_required(ADMIN_ROLES)
def update_lag(current_user, lag_id):
    """Update a team's information"""
    try:
        team = Lag.query.get_or_404(lag_id)
        data = request.get_json()

        if 'namn' in data:
            # Check if the new name already exists for another team
            existing = Lag.query.filter(Lag.namn == data['namn'], Lag.id != lag_id).first()
            if existing:
                return jsonify({"error": f"Team name '{data['namn']}' is already in use"}), 409

            team.namn = data['namn']

        db.session.commit()
        logger.info(f"Team updated: {team.namn} (id: {team.id}) by user {current_user.id}")

        return jsonify({
            "message": "Team updated successfully",
            "team": team.serialize()
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating team {lag_id}: {str(e)}")
        return jsonify({"error": f"Failed to update team: {str(e)}"}), 500


@lag_routes.route('/<int:lag_id>', methods=['DELETE'])
@token_required
@roles_required(ADMIN_ROLES)
def delete_lag(current_user, lag_id):
    """Delete a team"""
    try:
        team = Lag.query.get_or_404(lag_id)

        # Delete the team
        db.session.delete(team)
        db.session.commit()

        logger.info(f"Team deleted: {team.namn} (id: {lag_id}) by user {current_user.id}")
        return jsonify({"message": "Team deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting team {lag_id}: {str(e)}")
        return jsonify({"error": f"Failed to delete team: {str(e)}"}), 500


# ========== Team Membership Routes ==========

@lag_routes.route('/<int:lag_id>/users', methods=['POST'])
@token_required
@roles_required(COACH_ROLES)
def add_user_to_lag(current_user, lag_id):
    """Add a user to a team"""
    try:
        # Verify team exists
        team = Lag.query.get_or_404(lag_id)

        data = request.get_json()

        # Validate required fields
        required_fields = ['user_id', 'roll']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Field '{field}' is required"}), 400

        # Verify user exists
        user = User.query.get(data['user_id'])
        if not user:
            return jsonify({"error": f"User with ID {data['user_id']} not found"}), 404

        # Check if user is already in the team
        existing = db.session.query(user_lag).filter_by(
            user_id=data['user_id'],
            lag_id=lag_id
        ).first()

        if existing:
            return jsonify({"error": f"User is already a member of this team"}), 409

        # Add user to team
        user_team = user_lag.insert().values(
            user_id=data['user_id'],
            lag_id=lag_id,
            roll=data['roll'],
            position=data.get('position')
        )

        db.session.execute(user_team)
        db.session.commit()

        logger.info(f"User {data['user_id']} added to team {lag_id} as {data['roll']} by user {current_user.id}")

        return jsonify({
            "message": "User added to team successfully",
            "user_id": data['user_id'],
            "team_id": lag_id,
            "role": data['roll']
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error adding user to team {lag_id}: {str(e)}")
        return jsonify({"error": f"Failed to add user to team: {str(e)}"}), 500


@lag_routes.route('/<int:lag_id>/users/<int:user_id>', methods=['DELETE'])
@token_required
@roles_required(COACH_ROLES)
def remove_user_from_lag(current_user, lag_id, user_id):
    """Remove a user from a team"""
    try:
        # Verify team exists
        team = Lag.query.get_or_404(lag_id)

        # Verify user exists
        user = User.query.get_or_404(user_id)

        # Delete the relationship
        result = db.session.query(user_lag).filter_by(
            user_id=user_id,
            lag_id=lag_id
        ).delete()

        if result == 0:
            return jsonify({"error": "User is not a member of this team"}), 404

        db.session.commit()

        logger.info(f"User {user_id} removed from team {lag_id} by user {current_user.id}")
        return jsonify({"message": "User removed from team successfully"}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error removing user {user_id} from team {lag_id}: {str(e)}")
        return jsonify({"error": f"Failed to remove user from team: {str(e)}"}), 500


@lag_routes.route('/<int:lag_id>/users', methods=['GET'])
@token_required
def get_lag_users(current_user, lag_id):
    """Get all users in a team"""
    try:
        # Verify team exists
        team = Lag.query.get_or_404(lag_id)

        # Get all users in the team with their roles
        team_users = db.session.query(
            User, user_lag.c.roll, user_lag.c.position
        ).join(
            user_lag, User.id == user_lag.c.user_id
        ).filter(
            user_lag.c.lag_id == lag_id
        ).all()

        users_list = [{
            "id": user.id,
            "namn": user.namn,
            "email": user.email,
            "roll": roll,
            "position": position
        } for user, roll, position in team_users]

        return jsonify({
            "team": team.namn,
            "users": users_list
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving users for team {lag_id}: {str(e)}")
        return jsonify({"error": f"Failed to retrieve team users: {str(e)}"}), 500


@lag_routes.route('/<int:lag_id>/users/<int:user_id>', methods=['PUT'])
@token_required
@roles_required(COACH_ROLES)
def update_user_team_role(current_user, lag_id, user_id):
    """Update a user's role or position in a team"""
    try:
        data = request.get_json()

        # Verify team and user exist
        team = Lag.query.get_or_404(lag_id)
        user = User.query.get_or_404(user_id)

        # Check if user is in the team
        membership = db.session.query(user_lag).filter_by(
            user_id=user_id,
            lag_id=lag_id
        ).first()

        if not membership:
            return jsonify({"error": "User is not a member of this team"}), 404

        # Update role and/or position
        update_values = {}

        if 'roll' in data:
            update_values['roll'] = data['roll']

        if 'position' in data:
            update_values['position'] = data['position']

        if not update_values:
            return jsonify({"error": "No updates provided"}), 400

        # Perform update
        db.session.query(user_lag).filter_by(
            user_id=user_id,
            lag_id=lag_id
        ).update(update_values)

        db.session.commit()

        logger.info(f"User {user_id}'s role in team {lag_id} updated by user {current_user.id}")
        return jsonify({"message": "User's team role updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating user {user_id}'s role in team {lag_id}: {str(e)}")
        return jsonify({"error": f"Failed to update user's team role: {str(e)}"}), 500