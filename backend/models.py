from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'användare'
    id = db.Column("user_id", db.Integer, primary_key=True)
    namn = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    lösenord_hash = db.Column(db.String, nullable=False)

    def set_password(self, lösenord):
        self.lösenord_hash = generate_password_hash(lösenord)

    def check_password(self, lösenord):
        return check_password_hash(self.lösenord_hash, lösenord)

    def serialize(self):
        return {
            "id": self.id,
            "namn": self.namn,
            "email": self.email
        }

class Lag(db.Model):
    __tablename__ = 'lag'
    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100), nullable=False)
    skapad_datum = db.Column(db.DateTime, default=db.func.now())

    def serialize(self):
        return {
            "id": self.id,
            "namn": self.namn,
            "skapad_datum": self.skapad_datum.isoformat() if self.skapad_datum else None
        }
