# setup_postgres.py
import os
import sqlalchemy as sa
from sqlalchemy import create_engine, text
from app import create_app
from models import db, User

# Force PostgreSQL connection
os.environ['DATABASE_URL'] = 'postgresql://postgres:admin@localhost:5432/solvaders_fc'
app = create_app()  # This should create app with PostgreSQL connection

with app.app_context():
    # Verify we're using PostgreSQL
    if 'postgresql' not in str(db.engine.url):
        raise Exception(f"Not connected to PostgreSQL! Current connection: {db.engine.url}")

    print(f"✅ Connected to PostgreSQL: {db.engine.url}")

    # Recreate all tables
    db.drop_all()
    db.create_all()
    print("✅ Tables recreated in PostgreSQL")

    # Verify the roll column exists
    inspector = sa.inspect(db.engine)
    columns = inspector.get_columns('användare')
    column_names = [column['name'] for column in columns]

    if 'roll' in column_names:
        print("✅ 'roll' column exists in PostgreSQL användare table")
    else:
        print("❌ 'roll' column is missing from PostgreSQL!")