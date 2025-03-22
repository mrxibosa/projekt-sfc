from flask import jsonify


def register_error_handlers(app):
    """Registrerar felhanterare för vanliga HTTP-fel."""

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "error": "Bad Request",
            "message": "Begäran kunde inte förstås av servern på grund av felaktig syntax"
        }), 400

    @app.errorhandler(401)
    def unauthorized(error):
        return jsonify({
            "error": "Unauthorized",
            "message": "Autentisering krävs för att komma åt denna resurs"
        }), 401

    @app.errorhandler(403)
    def forbidden(error):
        return jsonify({
            "error": "Forbidden",
            "message": "Du har inte behörighet att utföra denna åtgärd"
        }), 403

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "error": "Not Found",
            "message": "Den begärda resursen kunde inte hittas på servern"
        }), 404

    @app.errorhandler(405)
    def method_not_allowed(error):
        return jsonify({
            "error": "Method Not Allowed",
            "message": "Den begärda metoden stöds inte för den begärda resursen"
        }), 405

    @app.errorhandler(422)
    def unprocessable_entity(error):
        return jsonify({
            "error": "Unprocessable Entity",
            "message": "Servern förstår innehållstypen men kunde inte bearbeta instruktionerna"
        }), 422

    @app.errorhandler(429)
    def too_many_requests(error):
        return jsonify({
            "error": "Too Many Requests",
            "message": "Du har skickat för många förfrågningar. Försök igen senare"
        }), 429

    @app.errorhandler(500)
    def internal_server_error(error):
        return jsonify({
            "error": "Internal Server Error",
            "message": "Ett internt serverfel har inträffat"
        }), 500

    @app.errorhandler(503)
    def service_unavailable(error):
        return jsonify({
            "error": "Service Unavailable",
            "message": "Servern är för närvarande inte tillgänglig"
        }), 503