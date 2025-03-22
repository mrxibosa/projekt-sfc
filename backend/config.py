# config.py
import os
from dotenv import load_dotenv

load_dotenv()  # 🔁 Laddar alla variabler från .env-filen

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret")
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///default.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
