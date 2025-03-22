from functools import wraps
from flask import request, jsonify
from datetime import datetime


def validate_json(required_fields=None):
    """Decorator för att validera JSON-data i request"""

    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Kontrollera att det finns JSON-data
            if not request.is_json:
                return jsonify({'error': 'JSON-data krävs'}), 400

            data = request.get_json()

            # Om inga specifika fält angetts, validera bara att det är giltig JSON
            if not required_fields:
                return f(*args, **kwargs)

            # Kontrollera att alla obligatoriska fält finns
            missing_fields = [field for field in required_fields if field not in data]

            if missing_fields:
                return jsonify({
                    'error': f'Följande obligatoriska fält saknas: {", ".join(missing_fields)}'
                }), 400

            return f(*args, **kwargs)

        return decorated_function

    return decorator


def validate_password(password):
    """Validera lösenord mot säkerhetskrav"""
    errors = []

    if len(password) < 8:
        errors.append("Lösenordet måste vara minst 8 tecken långt")

    if not any(char.isdigit() for char in password):
        errors.append("Lösenordet måste innehålla minst en siffra")

    if not any(char.isupper() for char in password):
        errors.append("Lösenordet måste innehålla minst en stor bokstav")

    if not any(char.islower() for char in password):
        errors.append("Lösenordet måste innehålla minst en liten bokstav")

    return errors


def validate_date(date_str):
    """Validera ett datum i ISO 8601-format"""
    try:
        date = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        return True, date
    except ValueError:
        return False, None