import os
from dotenv import load_dotenv

load_dotenv()

APP_ENV = os.getenv("APP_ENV", "development")

APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
APP_PORT = int(os.getenv("APP_PORT", 8000))

DEBUG = APP_ENV == "development"

DATABASE_TYPE = os.getenv("DATABASE_TYPE", "sqlite")
DATABASE_PATH = os.getenv("DATABASE_PATH", "./ads.db")

DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
DATABASE_PORT = os.getenv("DATABASE_PORT", "5432")
DATABASE_NAME = os.getenv("DATABASE_NAME", "ads_platform")
DATABASE_USER = os.getenv("DATABASE_USER", "ads_user")
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD", "ads_password")

SECRET_KEY = os.getenv("SECRET_KEY", "unsafe-development-key")