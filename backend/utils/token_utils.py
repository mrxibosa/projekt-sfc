from functools import wraps
from flask import request, jsonify
import jwt
from config import Config
from models import User


def token_required(f):
    """Decorator för att skydda routes med JWT-tokens"""

    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        # Hämta token från Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            if auth_header.startswith('Bearer '):
                token = auth_header.split(' ')[1]

        if not token:
            return jsonify({'error': 'Token saknas, autentisering krävs'}), 401

        try:
            # Avkoda token för att få användar-ID
            data = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.get(data['user_id'])

            if not current_user:
                return jsonify({'error': 'Ogiltig token, användaren finns inte'}), 401

        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token har gått ut, logga in igen'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Ogiltig token'}), 401

        # Skicka med användarobjektet till funktionen
        return f(current_user=current_user, *args, **kwargs)

    return decorated


def roles_required(allowed_roles):
    """Decorator för att kontrollera användarroller"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = kwargs.get('current_user')

            if not current_user:
                return jsonify({'error': 'Användare saknas'}), 401

            if current_user.roll not in allowed_roles:
                return jsonify({'error': 'Otillräcklig behörighet för denna åtgärd'}), 403

            return f(*args, **kwargs)

        return decorated_function

    return decorator