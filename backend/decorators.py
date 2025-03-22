from flask import request, jsonify
from functools import wraps
import jwt
from models import User
from config import Config


def token_required(f):
    """Decorator för att säkerställa att en giltig JWT-token finns med i begäran."""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Kontrollera om token finns i headers
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token saknas'}), 401

        try:
            # Avkoda token och hämta user_id
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])

            if not current_user:
                return jsonify({'error': 'Ogiltig token - användaren hittades inte'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token har löpt ut'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Ogiltig token'}), 401

        # Skicka med användaren till den dekorerade funktionen
        return f(current_user, *args, **kwargs)

    return decorated


def roles_required(allowed_roles):
    """Decorator för att kontrollera användarroller."""

    def decorator(f):
        @wraps(f)
        def decorated_function(current_user, *args, **kwargs):
            # Konvertera till lista om en sträng skickas in
            if isinstance(allowed_roles, str):
                roles = [allowed_roles]
            else:
                roles = allowed_roles

            if current_user.roll not in roles:
                return jsonify({
                    'error': 'Åtkomst nekad',
                    'message': 'Du har inte behörighet för denna åtgärd'
                }), 403

            return f(current_user, *args, **kwargs)

        return decorated_function

    return decorator