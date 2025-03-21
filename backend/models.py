from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'användare'
    id = db.Column("user_id", db.Integer, primary_key=True)
    namn = db.Column("namn", db.String(255), nullable=False)
    email = db.Column("email", db.String(255), unique=True, nullable=False)
    lösenord_hash = db.Column("lösenord_hash", db.String, nullable=False)

    def serialize(self):
        return {
            "id": self.id,
            "namn": self.namn,
            "email": self.email
        }

# Lägg till denna klass nedan:
class Lag(db.Model):
    __tablename__ = 'lag'
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100), nullable=False)
    skapad_datum = db.Column(db.DateTime, default=db.func.now())

    def serialize(self):
        return {
            "id": self.id,
            "namn": self.namn,
            "skapad_datum": self.skapad_datum.isoformat()
        }
