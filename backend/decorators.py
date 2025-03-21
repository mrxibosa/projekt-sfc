from flask import request, jsonify
import jwt
import os
from functools import wraps
from models import User

SECRET_KEY = os.getenv("SECRET_KEY", "superhemlignyckel")

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token saknas"}), 403

        try:
            token = token.replace("Bearer ", "")
            decoded_token = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = User.query.get(decoded_token["user_id"])
            if not user:
                return jsonify({"error": "Ogiltig token"}), 403
        except jwt.ExpiredSignatureError:
            return jsonify({"error": "Token har gått ut"}), 403
        except jwt.InvalidTokenError:
            return jsonify({"error": "Ogiltig token"}), 403

        return f(user, *args, **kwargs)
    return decorated
