from app import app, db  # Import both app and db
from models import User

# Wrap everything in an application context
with app.app_context():
    # Predefined users and roles
    users = [
        {"namn": "Super Admin", "email": "superadmin@example.com", "password": "superadmin123", "roll": "superadmin"},
        {"namn": "Admin User", "email": "admin@example.com", "password": "admin123", "roll": "admin"},
        {"namn": "Tränare User", "email": "tranare@example.com", "password": "tranare123", "roll": "tränare"},
        {"namn": "Spelare User", "email": "spelare@example.com", "password": "spelare123", "roll": "spelare"},
        {"namn": "Gäst User", "email": "gast@example.com", "password": "gast123", "roll": "gäst"}
    ]

    # Insert users into database
    for user_data in users:
        existing_user = User.query.filter_by(email=user_data["email"]).first()
        if not existing_user:
            new_user = User(namn=user_data["namn"], email=user_data["email"], roll=user_data["roll"])
            new_user.set_password(user_data["password"])  # Hash password
            db.session.add(new_user)
            print(f"✅ Adding user: {user_data['namn']} ({user_data['roll']})")
        else:
            print(f"⚠️ User already exists: {user_data['email']}")

    # Commit changes
    db.session.commit()
    print("✅ All users inserted successfully!")