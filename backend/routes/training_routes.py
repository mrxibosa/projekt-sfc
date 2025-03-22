from flask import Blueprint, request, jsonify
from models import db, Träning, Lag
from datetime import datetime
from decorators import token_required, roles_required
import logging

# Create blueprint
training_routes = Blueprint('training_routes', __name__)

# Set up logging
logger = logging.getLogger(__name__)


# Helper function for date parsing
def parse_date(date_string):
    try:
        # Handle different date formats including with or without timezone
        if date_string.endswith('Z'):
            date_string = date_string.replace('Z', '+00:00')
        return datetime.fromisoformat(date_string)
    except ValueError as e:
        logger.error(f"Date parsing error: {e}")
        return None


# ========== Training Routes ==========

@training_routes.route('/', methods=['POST'])
@token_required
@roles_required(['admin', 'tränare', 'superadmin'])
def create_training(current_user):
    """Create a new training session"""
    try:
        data = request.get_json()

        # Validate request data
        required_fields = ['lag_id', 'datum', 'typ']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({
                "error": "Missing required fields",
                "fields": missing_fields
            }), 400

        # Parse date
        training_date = parse_date(data['datum'])
        if not training_date:
            return jsonify({"error": "Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}), 400

        # Verify team exists
        team = Lag.query.get(data['lag_id'])
        if not team:
            return jsonify({"error": f"Team with ID {data['lag_id']} not found"}), 404

        # Create new training session
        new_training = Träning(
            lag_id=data['lag_id'],
            datum=training_date,
            typ=data['typ'],
            närvaro=data.get('närvaro', 0)
        )

        db.session.add(new_training)
        db.session.commit()

        logger.info(f"Training session created: {new_training.id} for team {team.namn}")
        return jsonify({
            "message": "Training session created successfully",
            "training": new_training.serialize()
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating training session: {str(e)}")
        return jsonify({"error": "An error occurred while creating the training session"}), 500


@training_routes.route('/', methods=['GET'])
@token_required
def get_all_trainings(current_user):
    """Get all training sessions with optional filtering"""
    try:
        # Support filtering by query parameters
        filters = {}

        # Filter by team id if provided
        lag_id = request.args.get('lag_id')
        if lag_id:
            try:
                filters['lag_id'] = int(lag_id)
            except ValueError:
                return jsonify({"error": "Invalid lag_id parameter"}), 400

        # Filter by training type if provided
        typ = request.args.get('typ')
        if typ:
            filters['typ'] = typ

        # Apply date filtering if provided
        query = Träning.query.filter_by(**filters)

        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')

        if from_date:
            from_date_obj = parse_date(from_date)
            if from_date_obj:
                query = query.filter(Träning.datum >= from_date_obj)

        if to_date:
            to_date_obj = parse_date(to_date)
            if to_date_obj:
                query = query.filter(Träning.datum <= to_date_obj)

        # Apply sorting
        sort_by = request.args.get('sort_by', 'datum')
        sort_order = request.args.get('sort_order', 'asc')

        if sort_by not in ['datum', 'id', 'lag_id', 'typ', 'närvaro']:
            sort_by = 'datum'  # Default sort

        if sort_order.lower() == 'desc':
            query = query.order_by(getattr(Träning, sort_by).desc())
        else:
            query = query.order_by(getattr(Träning, sort_by).asc())

        # Get paginated results
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        pagination = query.paginate(page=page, per_page=per_page)

        trainings = pagination.items

        return jsonify({
            "trainings": [training.serialize() for training in trainings],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving training sessions: {str(e)}")
        return jsonify({"error": "An error occurred while retrieving training sessions"}), 500


@training_routes.route('/<int:training_id>', methods=['GET'])
@token_required
def get_training(current_user, training_id):
    """Get a specific training session by ID"""
    try:
        training = Träning.query.get_or_404(training_id)
        return jsonify({"training": training.serialize()}), 200
    except Exception as e:
        logger.error(f"Error retrieving training session {training_id}: {str(e)}")
        return jsonify({"error": "An error occurred while retrieving the training session"}), 500


@training_routes.route('/lag/<int:lag_id>', methods=['GET'])
@token_required
def get_team_trainings(current_user, lag_id):
    """Get all training sessions for a specific team"""
    try:
        # Verify team exists
        team = Lag.query.get_or_404(lag_id)

        # Get paginated results
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        # Apply filtering
        query = Träning.query.filter_by(lag_id=lag_id)

        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')

        if from_date:
            from_date_obj = parse_date(from_date)
            if from_date_obj:
                query = query.filter(Träning.datum >= from_date_obj)

        if to_date:
            to_date_obj = parse_date(to_date)
            if to_date_obj:
                query = query.filter(Träning.datum <= to_date_obj)

        typ = request.args.get('typ')
        if typ:
            query = query.filter(Träning.typ == typ)

        # Apply sorting
        sort_by = request.args.get('sort_by', 'datum')
        sort_order = request.args.get('sort_order', 'asc')

        if sort_order.lower() == 'desc':
            query = query.order_by(getattr(Träning, sort_by).desc())
        else:
            query = query.order_by(getattr(Träning, sort_by).asc())

        pagination = query.paginate(page=page, per_page=per_page)
        trainings = pagination.items

        return jsonify({
            "team": team.namn,
            "trainings": [training.serialize() for training in trainings],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving training sessions for team {lag_id}: {str(e)}")
        return jsonify({"error": "An error occurred while retrieving team training sessions"}), 500


@training_routes.route('/<int:training_id>', methods=['PUT'])
@token_required
@roles_required(['admin', 'tränare', 'superadmin'])
def update_training(current_user, training_id):
    """Update a specific training session"""
    try:
        training = Träning.query.get_or_404(training_id)
        data = request.get_json()

        # Update fields if they exist in the request
        if 'datum' in data:
            training_date = parse_date(data['datum'])
            if not training_date:
                return jsonify({"error": "Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}), 400
            training.datum = training_date

        if 'typ' in data:
            training.typ = data['typ']

        if 'närvaro' in data:
            training.närvaro = data['närvaro']

        # Optionally allow changing the team
        if 'lag_id' in data:
            team = Lag.query.get(data['lag_id'])
            if not team:
                return jsonify({"error": f"Team with ID {data['lag_id']} not found"}), 404
            training.lag_id = data['lag_id']

        db.session.commit()
        logger.info(f"Training session updated: {training.id}")
        return jsonify({
            "message": "Training session updated successfully",
            "training": training.serialize()
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating training session {training_id}: {str(e)}")
        return jsonify({"error": "An error occurred while updating the training session"}), 500


@training_routes.route('/<int:training_id>/narvaro', methods=['POST'])
@token_required
@roles_required(['admin', 'tränare', 'superadmin'])
def record_attendance(current_user, training_id):
    """Record attendance for a specific training session"""
    try:
        training = Träning.query.get_or_404(training_id)
        data = request.get_json()

        if 'närvaro' not in data:
            return jsonify({"error": "Field 'närvaro' is required"}), 400

        try:
            närvaro = int(data['närvaro'])
        except ValueError:
            return jsonify({"error": "Attendance must be a number"}), 400

        training.närvaro = närvaro
        db.session.commit()

        logger.info(f"Attendance recorded for training session {training.id}: {närvaro}")
        return jsonify({
            "message": "Attendance recorded successfully",
            "training": training.serialize()
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error recording attendance for training session {training_id}: {str(e)}")
        return jsonify({"error": "An error occurred while recording attendance"}), 500


@training_routes.route('/<int:training_id>', methods=['DELETE'])
@token_required
@roles_required(['admin', 'superadmin'])
def delete_training(current_user, training_id):
    """Delete a specific training session"""
    try:
        training = Träning.query.get_or_404(training_id)
        db.session.delete(training)
        db.session.commit()
        logger.info(f"Training session deleted: {training_id}")
        return jsonify({"message": "Training session deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting training session {training_id}: {str(e)}")
        return jsonify({"error": "An error occurred while deleting the training session"})