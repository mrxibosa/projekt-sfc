# add_users_to_postgres.py
import os
import psycopg2
from psycopg2.extras import DictCursor
from werkzeug.security import generate_password_hash

# Direct PostgreSQL connection using psycopg2
conn = psycopg2.connect(
    dbname="solvaders_fc",
    user="postgres",
    password="admin",
    host="localhost"
)
conn.autocommit = False
cursor = conn.cursor(cursor_factory=DictCursor)

# Define user data
users = [
    {"namn": "Super Admin", "email": "superadmin@example.com", "password": "superadmin123", "roll": "superadmin"},
    {"namn": "Admin User", "email": "admin@example.com", "password": "admin123", "roll": "admin"},
    {"namn": "Tränare User", "email": "tranare@example.com", "password": "tranare123", "roll": "tränare"},
    {"namn": "Spelare User", "email": "spelare@example.com", "password": "spelare123", "roll": "spelare"},
    {"namn": "Gäst User", "email": "gast@example.com", "password": "gast123", "roll": "gäst"}
]

try:
    # Check if users already exist
    cursor.execute("SELECT COUNT(*) FROM användare")
    existing_count = cursor.fetchone()[0]
    print(f"Found {existing_count} existing users in PostgreSQL")

    # Add users if none exist
    if existing_count == 0:
        for user_data in users:
            # Create user with hashed password
            password_hash = generate_password_hash(user_data["password"])

            cursor.execute(
                "INSERT INTO användare (namn, email, lösenord_hash, roll) VALUES (%s, %s, %s, %s)",
                (user_data["namn"], user_data["email"], password_hash, user_data["roll"])
            )
            print(f"✅ Adding user: {user_data['namn']} ({user_data['roll']})")

        # Commit changes
        conn.commit()
        print("✅ All users inserted successfully to PostgreSQL!")

        # Verify users were added
        cursor.execute("SELECT COUNT(*) FROM användare")
        user_count = cursor.fetchone()[0]
        print(f"PostgreSQL now has {user_count} users")
    else:
        print("Users already exist in PostgreSQL, no action taken")

except Exception as e:
    conn.rollback()
    print(f"❌ Error: {e}")
finally:
    cursor.close()
    conn.close()