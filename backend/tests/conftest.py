import pytest
from app import create_app
from models import db, User
from werkzeug.security import generate_password_hash
import os


@pytest.fixture(scope='function')
def app():
    """Skapa och konfigurera Flask-applikation för testning"""
    # Använd en separat testdatabas för PostgreSQL
    os.environ['TEST_DATABASE_URL'] = 'postgresql://postgres:admin@localhost:5432/solvaders_fc_test'

    # Skapa app med testflaggan
    app = create_app(testing=True)

    # Skapa testdatabasstrukturen
    with app.app_context():
        db.drop_all()  # Rensa befintliga tabeller först
        db.create_all()

        # Skapa testdata: admin-användare
        admin = User(
            förnamn="Admin",
            efternamn="Testsson",
            email="admin@test.com",
            lösenord="Testpassword1",
            roll="admin"
        )

        # Vanlig användare
        user = User(
            förnamn="Vanlig",
            efternamn="Användarsson",
            email="user@test.com",
            lösenord="Testpassword1",
            roll="spelare"
        )

        db.session.add(admin)
        db.session.add(user)
        db.session.commit()

    yield app

    # Rensa databasen efter testet
    with app.app_context():
        db.session.remove()
        db.drop_all()


@pytest.fixture(scope='function')
def client(app):
    """Skapa en testklient för Flask-applikationen"""
    return app.test_client()


@pytest.fixture(scope='function')
def runner(app):
    """Skapa en testrunner för Flask CLI-kommandon"""
    return app.test_cli_runner()


@pytest.fixture(scope='function')
def admin_token(client):
    """Skapa en giltig admin-token för testning"""
    response = client.post('/auth/login', json={
        'email': 'admin@test.com',
        'lösenord': 'Testpassword1'
    })
    return response.json['token']


@pytest.fixture(scope='function')
def user_token(client):
    """Skapa en giltig användar-token för testning"""
    response = client.post('/auth/login', json={
        'email': 'user@test.com',
        'lösenord': 'Testpassword1'
    })
    return response.json['token']