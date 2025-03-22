from flask import Flask
from flask_migrate import Migrate
import os
from models import db
from utils.error_handlers import register_error_handlers
from config import Config, TestConfig

def create_app(testing=False):
    """Factory method to create and configure the Flask application."""
    app = Flask(__name__)

    # Välj konfiguration baserat på miljö
    if testing:
        app.config.from_object(TestConfig)
    else:
        app.config.from_object(Config)

    # Fixa PostgreSQL URL för Heroku-kompatibilitet
    database_url = app.config['SQLALCHEMY_DATABASE_URI']
    if database_url and database_url.startswith('postgres://'):
        app.config['SQLALCHEMY_DATABASE_URI'] = database_url.replace('postgres://', 'postgresql://', 1)

    # Initialize the database and Flask-Migrate
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register error handlers
    register_error_handlers(app)

    # Register Blueprints for different routes
    # VIKTIGT: Importera Blueprints efter att app är skapad för att undvika cirkulära importer
    with app.app_context():
        from routes.auth_routes import auth_routes
        from routes.user_routes import user_routes
        from routes.lag_routes import lag_routes
        from routes.match_routes import match_routes
        from routes.training_routes import training_routes

        app.register_blueprint(auth_routes, url_prefix='/auth')
        app.register_blueprint(user_routes, url_prefix='/users')
        app.register_blueprint(lag_routes, url_prefix='/lag')
        app.register_blueprint(match_routes, url_prefix='/matcher')
        app.register_blueprint(training_routes, url_prefix='/traningar')

    return app

# Create a global app instance for Flask CLI
app = create_app()

# Application entry point
if __name__ == "__main__":
    print(f"Database URL: {app.config['SQLALCHEMY_DATABASE_URI']}")
    print(app.url_map)  # Display all registered routes for debugging
    app.run(debug=True, host='0.0.0.0', port=5000)