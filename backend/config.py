import os
from datetime import timedelta

class Config:
    """Baskonfiguration för applikationen"""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'en-mycket-hemlig-nyckel'
    # PostgreSQL-konfiguration med solvaders_fc databas
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or 'postgresql://postgres:admin@localhost:5432/solvaders_fc'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-hemlig-nyckel'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)

class TestConfig(Config):
    """Konfiguration för testmiljön"""
    TESTING = True
    # Använd test-databas för tester
    SQLALCHEMY_DATABASE_URI = os.environ.get('TEST_DATABASE_URL') or 'postgresql://postgres:admin@localhost:5432/solvaders_fc_test'
    WTF_CSRF_ENABLED = False