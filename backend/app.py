from flask import Flask
from models import db
from routes.auth_routes import auth_routes
from routes.user_routes import user_routes
from routes.lag_routes import lag_routes
import os

def create_app():
    """Skapar och konfigurerar Flask-applikationen."""
    app = Flask(__name__)

    # Konfiguration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
        'DATABASE_URL', 'postgresql://postgres:admin@localhost:5432/solvaders_fc'
    )
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv("SECRET_KEY", "superhemlignyckel")

    # Initiera databas
    db.init_app(app)

    # Registrera Blueprints
    app.register_blueprint(auth_routes, url_prefix='/auth')
    app.register_blueprint(user_routes, url_prefix='/users')
    app.register_blueprint(lag_routes, url_prefix='/lag')

    return app

if __name__ == '__main__':
    app = create_app()
    print(app.url_map)  # Debug: visar alla registrerade routes
    app.run(debug=True, host='0.0.0.0', port=5000)
