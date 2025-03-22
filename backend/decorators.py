from functools import wraps
from flask import jsonify, request
import jwt
from models import User

# Use the same SECRET_KEY as auth_routes.py
SECRET_KEY = "superhemlignyckel"

def token_required(f):
    """
    Decorator that checks if a valid JWT token is present in the request
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Check if token is in headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({"error": "Token is missing"}), 401

        try:
            # Decode the token using the same SECRET_KEY as auth_routes.py
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])

            # Get the user from the database
            current_user = User.query.filter_by(id=data['user_id']).first()

            if not current_user:
                return jsonify({"error": "User not found"}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token has expired"}), 401
        except jwt.InvalidTokenError:
            return jsonify({"error": "Invalid token"}), 401

        # Pass the current user to the route function
        return f(current_user, *args, **kwargs)

    return decorated


def roles_required(allowed_roles):
    """
    Decorator that checks if the current user has one of the allowed roles

    Args:
        allowed_roles (list): List of role names that are allowed to access the route
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            # Check if user's role is in the allowed roles
            if not current_user.roll in allowed_roles:
                return jsonify({
                    "error": "Permission denied",
                    "message": f"This action requires one of these roles: {', '.join(allowed_roles)}"
                }), 403

            return f(current_user, *args, **kwargs)

        return decorated_function

    return decorator