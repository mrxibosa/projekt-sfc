from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

# Initialize the database instance
db = SQLAlchemy()

# 🔹 Many-to-Many relationship between User and Lag
user_lag = db.Table(
    'user_lag',
    db.Column('user_id', db.Integer, db.ForeignKey('användare.user_id'), primary_key=True),
    db.Column('lag_id', db.Integer, db.ForeignKey('lag.lag_id'), primary_key=True),
    db.Column('roll', db.String(50), nullable=False, default='spelare'),  # E.g., 'tränare', 'spelare'
    db.Column('position', db.String(100), nullable=True),  # E.g., 'anfallare', 'målvakt'
    db.Column('skapad_datum', db.DateTime, default=datetime.utcnow)  # When the role was assigned
)

# 🟢 User Model
class User(db.Model):
    __tablename__ = 'användare'

    id = db.Column("user_id", db.Integer, primary_key=True)
    namn = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    lösenord_hash = db.Column(db.String, nullable=False)
    roll = db.Column(db.String(50), nullable=False, default="spelare")  # Default role

    lag = db.relationship('Lag', secondary=user_lag, back_populates='medlemmar')

    def set_password(self, lösenord):
        """ Hashar och sparar lösenordet """
        self.lösenord_hash = generate_password_hash(lösenord)

    def check_password(self, lösenord):
        """ Jämför inskrivet lösenord med det hashade lösenordet """
        return check_password_hash(self.lösenord_hash, lösenord)

    def serialize(self):
        """ Returnerar användaren i JSON-format """
        return {
            "id": self.id,
            "namn": self.namn,
            "email": self.email,
            "roll": self.roll
        }


# 🔹 Lag Model
class Lag(db.Model):
    __tablename__ = 'lag'

    id = db.Column("lag_id", db.Integer, primary_key=True)
    namn = db.Column(db.String(255), nullable=False, unique=True)
    skapad_datum = db.Column(db.DateTime, server_default=db.func.now())

    medlemmar = db.relationship('User', secondary=user_lag, back_populates='lag')

    def serialize(self):
        """ Returnerar laget i JSON-format utan medlemmar """
        return {
            "id": self.id,
            "namn": self.namn,
            "skapad_datum": self.skapad_datum.strftime('%Y-%m-%d %H:%M:%S')
        }

    def serialize_with_members(self):
        """ Returnerar laget i JSON-format med medlemmar """
        return {
            **self.serialize(),
            "medlemmar": [user.serialize() for user in self.medlemmar]
        }


# 🔥 Match Model
class Match(db.Model):
    __tablename__ = 'matcher'

    id = db.Column("match_id", db.Integer, primary_key=True)
    lag_id = db.Column(db.Integer, db.ForeignKey('lag.lag_id'), nullable=False)
    datum = db.Column(db.DateTime, nullable=False)
    plats = db.Column(db.String(255), nullable=False)
    motståndarlag = db.Column(db.String(255), nullable=False)

    lag = db.relationship('Lag', backref=db.backref('matcher', lazy=True))

    def serialize(self):
        """ Returnerar matchen i JSON-format """
        return {
            "id": self.id,
            "lag": self.lag.namn,
            "datum": self.datum.strftime('%Y-%m-%d %H:%M:%S'),
            "plats": self.plats,
            "motståndarlag": self.motståndarlag
        }


# 🔥 Träning Model
class Träning(db.Model):
    __tablename__ = 'träningar'

    id = db.Column("träning_id", db.Integer, primary_key=True)
    lag_id = db.Column(db.Integer, db.ForeignKey('lag.lag_id'), nullable=False)
    datum = db.Column(db.DateTime, nullable=False)
    typ = db.Column(db.String(100), nullable=False)  # E.g., "Fys", "Teknik", "Spelövningar"
    närvaro = db.Column(db.Integer, default=0)  # Antal närvarande spelare

    lag = db.relationship('Lag', backref=db.backref('träningar', lazy=True))

    def serialize(self):
        """ Returnerar träningen i JSON-format """
        return {
            "id": self.id,
            "lag": self.lag.namn,
            "datum": self.datum.strftime('%Y-%m-%d %H:%M:%S'),
            "typ": self.typ,
            "närvaro": self.närvaro
        }
