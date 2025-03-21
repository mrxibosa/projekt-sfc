from flask import Flask, jsonify
from models import db, User, Lag
import os

# Initialize Flask application
app = Flask(__name__)

# Database configuration
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:admin@localhost:5432/solvaders_fc')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy with the Flask app
db.init_app(app)

# Route: Fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        users = User.query.all()
        return jsonify([{
            "id": user.id,
            "namn": user.namn,  # ändrat från username till namn
            "email": user.email
        } for user in users]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# Route: Fetch all lag (ny endpoint)
@app.route('/lag', methods=['GET'])
def get_lag():
    try:
        lag = Lag.query.all()
        return jsonify([l.serialize() for l in lag]), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
