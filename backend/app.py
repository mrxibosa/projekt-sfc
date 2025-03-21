from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
import os

# Initialize Flask application
app = Flask(__name__)

# Database configuration using environment variables for better security
DATABASE_URL = os.getenv('DATABASE_URL', 'postgresql://postgres:admin@localhost:5432/solvaders_fc')
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications to improve performance

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Model: User
class User(db.Model):
    __tablename__ = 'användare'  # Table name must exactly match, including quotes and special characters
    id = db.Column("user_id", db.Integer, primary_key=True)
    namn = db.Column("namn", db.String(255), nullable=False)
    email = db.Column("email", db.String(255), unique=True, nullable=False)
    lösenord_hash = db.Column("lösenord_hash", db.String, nullable=False)



# Route: Fetch all users
@app.route('/users', methods=['GET'])
def get_users():
    try:
        # Query all users and return in JSON format
        users = User.query.all()
        return jsonify([{"id": u.id, "namn": u.namn, "email": u.email} for u in users]), 200
    except Exception as e:
        # Handle errors gracefully
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Define host and port for scalability if deployed
    app.run(debug=True, host='0.0.0.0', port=5000)
