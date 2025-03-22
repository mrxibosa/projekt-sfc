from flask import Blueprint, request, jsonify
from models import db, Match, Lag
from datetime import datetime
from decorators import token_required, roles_required
import logging

# Create blueprint
match_routes = Blueprint('match_routes', __name__)

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


# ========== Match Routes ==========

@match_routes.route('/', methods=['POST'])
@token_required
@roles_required(['admin', 'tränare', 'superadmin'])
def create_match(current_user):
    """Create a new match"""
    try:
        data = request.get_json()

        # Validate request data
        required_fields = ['lag_id', 'datum', 'plats', 'motståndarlag']
        missing_fields = [field for field in required_fields if field not in data]

        if missing_fields:
            return jsonify({
                "error": "Missing required fields",
                "fields": missing_fields
            }), 400

        # Parse date
        match_date = parse_date(data['datum'])
        if not match_date:
            return jsonify({"error": "Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}), 400

        # Verify team exists
        team = Lag.query.get(data['lag_id'])
        if not team:
            return jsonify({"error": f"Team with ID {data['lag_id']} not found"}), 404

        # Create new match
        new_match = Match(
            lag_id=data['lag_id'],
            datum=match_date,
            plats=data['plats'],
            motståndarlag=data['motståndarlag']
        )

        db.session.add(new_match)
        db.session.commit()

        logger.info(f"Match created: {new_match.id} for team {team.namn}")
        return jsonify({
            "message": "Match created successfully",
            "match": new_match.serialize()
        }), 201

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error creating match: {str(e)}")
        return jsonify({"error": "An error occurred while creating the match"}), 500


@match_routes.route('/', methods=['GET'])
@token_required
def get_all_matches(current_user):
    """Get all matches with optional filtering"""
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

        # Filter by date range if provided
        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')

        query = Match.query.filter_by(**filters)

        if from_date:
            from_date_obj = parse_date(from_date)
            if from_date_obj:
                query = query.filter(Match.datum >= from_date_obj)

        if to_date:
            to_date_obj = parse_date(to_date)
            if to_date_obj:
                query = query.filter(Match.datum <= to_date_obj)

        # Apply sorting
        sort_by = request.args.get('sort_by', 'datum')
        sort_order = request.args.get('sort_order', 'asc')

        if sort_by not in ['datum', 'id', 'lag_id', 'plats', 'motståndarlag']:
            sort_by = 'datum'  # Default sort

        if sort_order.lower() == 'desc':
            query = query.order_by(getattr(Match, sort_by).desc())
        else:
            query = query.order_by(getattr(Match, sort_by).asc())

        # Get paginated results
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        pagination = query.paginate(page=page, per_page=per_page)

        matches = pagination.items

        return jsonify({
            "matches": [match.serialize() for match in matches],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving matches: {str(e)}")
        return jsonify({"error": "An error occurred while retrieving matches"}), 500


@match_routes.route('/<int:match_id>', methods=['GET'])
@token_required
def get_match(current_user, match_id):
    """Get a specific match by ID"""
    try:
        match = Match.query.get_or_404(match_id)
        return jsonify({"match": match.serialize()}), 200
    except Exception as e:
        logger.error(f"Error retrieving match {match_id}: {str(e)}")
        return jsonify({"error": "An error occurred while retrieving the match"}), 500


@match_routes.route('/lag/<int:lag_id>', methods=['GET'])
@token_required
def get_team_matches(current_user, lag_id):
    """Get all matches for a specific team"""
    try:
        # Verify team exists
        team = Lag.query.get_or_404(lag_id)

        # Get paginated results
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)

        # Apply date filtering if provided
        query = Match.query.filter_by(lag_id=lag_id)

        from_date = request.args.get('from_date')
        to_date = request.args.get('to_date')

        if from_date:
            from_date_obj = parse_date(from_date)
            if from_date_obj:
                query = query.filter(Match.datum >= from_date_obj)

        if to_date:
            to_date_obj = parse_date(to_date)
            if to_date_obj:
                query = query.filter(Match.datum <= to_date_obj)

        # Apply sorting
        sort_by = request.args.get('sort_by', 'datum')
        sort_order = request.args.get('sort_order', 'asc')

        if sort_order.lower() == 'desc':
            query = query.order_by(getattr(Match, sort_by).desc())
        else:
            query = query.order_by(getattr(Match, sort_by).asc())

        pagination = query.paginate(page=page, per_page=per_page)
        matches = pagination.items

        return jsonify({
            "team": team.namn,
            "matches": [match.serialize() for match in matches],
            "total": pagination.total,
            "pages": pagination.pages,
            "current_page": page
        }), 200

    except Exception as e:
        logger.error(f"Error retrieving matches for team {lag_id}: {str(e)}")
        return jsonify({"error": "An error occurred while retrieving team matches"}), 500


@match_routes.route('/<int:match_id>', methods=['PUT'])
@token_required
@roles_required(['admin', 'tränare', 'superadmin'])
def update_match(current_user, match_id):
    """Update a specific match"""
    try:
        match = Match.query.get_or_404(match_id)
        data = request.get_json()

        # Update fields if they exist in the request
        if 'datum' in data:
            match_date = parse_date(data['datum'])
            if not match_date:
                return jsonify({"error": "Invalid date format. Use ISO format (YYYY-MM-DDTHH:MM:SS)"}), 400
            match.datum = match_date

        if 'plats' in data:
            match.plats = data['plats']

        if 'motståndarlag' in data:
            match.motståndarlag = data['motståndarlag']

        # Optionally allow changing the team
        if 'lag_id' in data:
            team = Lag.query.get(data['lag_id'])
            if not team:
                return jsonify({"error": f"Team with ID {data['lag_id']} not found"}), 404
            match.lag_id = data['lag_id']

        db.session.commit()
        logger.info(f"Match updated: {match.id}")
        return jsonify({
            "message": "Match updated successfully",
            "match": match.serialize()
        }), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error updating match {match_id}: {str(e)}")
        return jsonify({"error": "An error occurred while updating the match"}), 500


@match_routes.route('/<int:match_id>', methods=['DELETE'])
@token_required
@roles_required(['admin', 'superadmin'])
def delete_match(current_user, match_id):
    """Delete a specific match"""
    try:
        match = Match.query.get_or_404(match_id)
        db.session.delete(match)
        db.session.commit()
        logger.info(f"Match deleted: {match_id}")
        return jsonify({"message": "Match deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        logger.error(f"Error deleting match {match_id}: {str(e)}")
        return jsonify({"error": "An error occurred while deleting the match"}), 500