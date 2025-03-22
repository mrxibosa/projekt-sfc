from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db  # Import your database instance from models.py
import os


def create_app():
    """Factory method to create and configure the Flask application."""
    app = Flask(__name__)

    # Flask app configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///app.db')  # Default to SQLite
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "super-secret-key")

    # Initialize the database and Flask-Migrate
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register Blueprints for different routes (moved down to avoid circular imports)
    from routes.auth_routes import auth_routes
    from routes.user_routes import user_routes
    from routes.lag_routes import lag_routes

    app.register_blueprint(auth_routes, url_prefix='/auth')
    app.register_blueprint(user_routes, url_prefix='/users')
    app.register_blueprint(lag_routes, url_prefix='/lag')

    return app


# Create a global app instance for Flask CLI
app = create_app()

# Application entry point
if __name__ == "__main__":
    print(app.url_map)  # Display all registered routes for debugging
    app.run(debug=True, host='0.0.0.0', port=5000)