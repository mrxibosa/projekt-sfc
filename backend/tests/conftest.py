# tests/conftest.py
import os
import sys

# Lägg till backend-mappen i sys.path
# Denna fil (conftest.py) ligger i backend/tests, så vi flyttar en nivå upp.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from app import create_app, db  # Nu bör modulen hittas
from models import User

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "SQLALCHEMY_TRACK_MODIFICATIONS": False
    })

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def test_user(app):
    user = User(namn="Testare", email="test@example.com", roll="admin")
    user.set_password("test123")
    db.session.add(user)
    db.session.commit()
    return user
