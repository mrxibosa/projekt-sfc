from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash

# Skapa databas-instans
db = SQLAlchemy()

# Associationstabell för många-till-många relation mellan User och Lag
user_lag = db.Table('user_lag',
                    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
                    db.Column('lag_id', db.Integer, db.ForeignKey('lag.id'), primary_key=True)
                    )


class User(db.Model):
    """Användarmodell för systemet"""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    förnamn = db.Column(db.String(50), nullable=False)
    efternamn = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    lösenord_hash = db.Column(db.String(200), nullable=False)
    telefon = db.Column(db.String(20), nullable=True)
    roll = db.Column(db.String(20), default='spelare')  # spelare, tränare, admin
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationer till andra tabeller
    # Fixad relation som specificerar foreign_keys
    träningar = db.relationship('Träning', backref='användare', lazy=True, foreign_keys='Träning.user_id')

    def __init__(self, förnamn, efternamn, email, lösenord, telefon=None, roll='spelare'):
        self.förnamn = förnamn
        self.efternamn = efternamn
        self.email = email
        self.lösenord_hash = generate_password_hash(lösenord)
        self.telefon = telefon
        self.roll = roll

    def __repr__(self):
        return f'<User {self.förnamn} {self.efternamn}>'

    # Lägg till serialize-metod för API-svar
    def serialize(self):
        return {
            'id': self.id,
            'förnamn': self.förnamn,
            'efternamn': self.efternamn,
            'email': self.email,
            'telefon': self.telefon,
            'roll': self.roll
        }


class Lag(db.Model):
    """Modell för lag"""
    __tablename__ = 'lag'

    id = db.Column(db.Integer, primary_key=True)
    namn = db.Column(db.String(100), nullable=False)
    beskrivning = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationer
    medlemmar = db.relationship('User', secondary=user_lag, backref=db.backref('lag', lazy='dynamic'))
    träningar = db.relationship('Träning', backref='lag', lazy=True)

    def __repr__(self):
        return f'<Lag {self.namn}>'


class Match(db.Model):
    """Modell för matcher"""
    __tablename__ = 'matcher'

    id = db.Column(db.Integer, primary_key=True)
    hemmalag_id = db.Column(db.Integer, db.ForeignKey('lag.id'), nullable=False)
    bortalag_id = db.Column(db.Integer, db.ForeignKey('lag.id'), nullable=False)
    datum = db.Column(db.DateTime, nullable=False)
    plats = db.Column(db.String(100), nullable=False)
    resultat_hemma = db.Column(db.Integer, nullable=True)
    resultat_borta = db.Column(db.Integer, nullable=True)

    # Relationer
    hemmalag = db.relationship('Lag', foreign_keys=[hemmalag_id])
    bortalag = db.relationship('Lag', foreign_keys=[bortalag_id])

    def __repr__(self):
        return f'<Match {self.hemmalag_id} vs {self.bortalag_id} at {self.datum}>'


class Träning(db.Model):
    """Modell för träningar"""
    __tablename__ = 'träningar'

    id = db.Column(db.Integer, primary_key=True)
    lag_id = db.Column(db.Integer, db.ForeignKey('lag.id'), nullable=False)
    # Lägg till foreign key för användare
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    datum = db.Column(db.DateTime, nullable=False)
    plats = db.Column(db.String(100), nullable=False)
    beskrivning = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f'<Träning för lag {self.lag_id} den {self.datum}>'

    # Lägg till serialize-metod för API-svar
    def serialize(self):
        return {
            'id': self.id,
            'lag_id': self.lag_id,
            'user_id': self.user_id,
            'datum': self.datum.isoformat() if self.datum else None,
            'plats': self.plats,
            'beskrivning': self.beskrivning
        }