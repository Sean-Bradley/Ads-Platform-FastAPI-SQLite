import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", 8000))

DEBUG = APP_ENV == "development"

DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
DATABASE_PATH = os.getenv("DATABASE_PATH", "./ads.db")

SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-development-key")