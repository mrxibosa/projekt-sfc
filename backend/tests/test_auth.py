# tests/test_auth.py
print("Running test_auth.py")

from models import db, User

def test_login_success(client, app):
    # Use app context to interact with the database
    with app.app_context():
        # Create a test user in the database
        user = User(
            förnamn="Test",  # Changed from namn to förnamn
            efternamn="User", # Added efternamn field
            email="test@example.com",
            lösenord="secret", # Changed to send actual password, not hash
            roll="användare"
        )
        db.session.add(user)
        db.session.commit()

    # Try logging in - note the endpoint and parameter names matching your API
    response = client.post("/auth/login", json={
        "email": "test@example.com",
        "lösenord": "secret"
    })

    assert response.status_code == 200
    assert "token" in response.get_json()