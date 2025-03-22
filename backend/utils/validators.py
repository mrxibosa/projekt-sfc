from flask import request, jsonify
from functools import wraps
from datetime import datetime

# ✅ Dekorator för att validera JSON-request
def validate_json(required_fields):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            data = request.get_json()
            if not data:
                return jsonify({"error": "Ingen JSON-data skickades"}), 400
            missing = [field for field in required_fields if field not in data]
            if missing:
                return jsonify({"error": "Fält saknas", "fields": missing}), 400
            return f(*args, **kwargs)
        return wrapper
    return decorator

# ✅ Funktion för att validera datum
def validate_date(date_string):
    try:
        if date_string.endswith("Z"):
            date_string = date_string.replace("Z", "+00:00")
        return datetime.fromisoformat(date_string)
    except Exception:
        return None
