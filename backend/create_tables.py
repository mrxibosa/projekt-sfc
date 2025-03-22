# create_tables.py
from app import app
from models import db, User, Lag, Match, Träning

with app.app_context():
    # Create all tables
    db.create_all()
    print("✅ Tables created successfully!")

    # Check if the 'roll' column exists in the User model
    inspector = db.inspect(db.engine)
    columns = inspector.get_columns('användare')
    column_names = [column['name'] for column in columns]

    if 'roll' in column_names:
        print("✅ 'roll' column exists in User model")
    else:
        print("❌ 'roll' column is missing!")