from flask import request, jsonify
import jwt
from functools import wraps
from models import User

SECRET_KEY = "superhemlignyckel"

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization', None)
        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Token saknas eller är ogiltig"}), 401

        try:
            token = token.split(" ")[1]
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            user = User.query.get(data['user_id'])
            if not user:
                return jsonify({"error": "Ogiltig användare"}), 401
        except Exception:
            return jsonify({"error": "Token är ogiltig eller har gått ut"}), 401

        return f(user, *args, **kwargs)
    return decorated
