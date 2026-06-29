import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Flask settings
    PORT = int(os.getenv("PORT", 5000))
    ENV = os.getenv("FLASK_ENV", "development")
    DEBUG = ENV == "development"
    
    # Database Settings (GIMS currently uses SQLite via db.py, 
    # but these are kept for future MySQL scaling)
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = int(os.getenv("DB_PORT", 3306))
    DB_USER = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "")
    DB_NAME = os.getenv("DB_NAME", "gims_db")
    
    # JWT authentication settings
    JWT_SECRET = os.getenv("JWT_SECRET")
    JWT_EXPIRES_IN = int(os.getenv("JWT_EXPIRES_IN", 86400))  # Default 24 hours
    
    # CORS Origin Whitelist
    CORS_ORIGIN = os.getenv("CORS_ORIGIN", "http://localhost:3000")
    
    if not JWT_SECRET:
        raise ValueError("CRITICAL: JWT_SECRET environment variable is missing!")

