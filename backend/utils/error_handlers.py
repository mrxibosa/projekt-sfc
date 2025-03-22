# error_handlers.py or utils/error_handlers.py
from flask import jsonify


def register_error_handlers(app):
    """Register error handlers for the Flask app"""

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad Request",
            "message": str(error)
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "error": "Unauthorized",
            "message": "Authentication required for this function"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "error": "Forbidden",
            "message": "You don't have sufficient permissions for this action"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Resource not found",
            "message": str(error)
        }), 404

    @app.errorhandler(500)
    def server_error(error):
        return jsonify({
            "error": "Server Error",
            "message": "An unexpected error occurred. Please try again later."
        }), 500