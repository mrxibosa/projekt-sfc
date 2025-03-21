from app import create_app  # Importera create_app-funktionen istället för en app-variabel
from models import db
from sqlalchemy import text  # Viktigt! För att köra rå SQL i SQLAlchemy 2.x

# Skapa en app-instans via create_app()
app = create_app()

with app.app_context():
    # Ta bort tabeller i rätt ordning (anpassa vid behov)
    db.session.execute(text("DROP TABLE IF EXISTS träning CASCADE;"))
    db.session.execute(text("DROP TABLE IF EXISTS lag CASCADE;"))
    db.session.execute(text("DROP TABLE IF EXISTS användare CASCADE;"))

    db.session.commit()  # Viktigt! Spara ändringar i databasen

    # Skapa om alla tabeller
    db.create_all()
    print("✅ Alla tabeller har skapats om!")
