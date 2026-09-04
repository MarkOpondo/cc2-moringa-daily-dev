import os
from pathlib import Path

from dotenv import load_dotenv


BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env", override=True)


def database_uri():
    """Build a database URL from DATABASE_URL or the documented DB_* values."""
    if os.environ.get("DATABASE_URL"):
        return os.environ["DATABASE_URL"]

    db_name = os.environ.get("DB_NAME")
    if db_name:
        user = os.environ.get("DB_USER", "postgres")
        password = os.environ.get("DB_PASSWORD", "")
        host = os.environ.get("DB_HOST", "localhost")
        port = os.environ.get("DB_PORT", "5432")
        credentials = f"{user}:{password}@" if password else f"{user}@"
        return f"postgresql+psycopg2://{credentials}{host}:{port}/{db_name}"

    # SQLite makes a fresh checkout runnable without requiring PostgreSQL.
    instance_dir = BASE_DIR / "instance"
    instance_dir.mkdir(exist_ok=True)
    return f"sqlite:///{instance_dir / 'moringa_daily_dev.sqlite3'}"


class Config:
    SECRET_KEY = os.environ.get(
        "SECRET_KEY", "dev-secret-key-change-in-production-please"
    )
    JWT_SECRET_KEY = os.environ.get(
        "JWT_SECRET_KEY", "jwt-secret-change-in-production-please"
    )
    SQLALCHEMY_DATABASE_URI = database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    FRONTEND_URL = os.environ.get("FRONTEND_URL", "http://localhost:5173")
    PASSWORD_RESET_TOKEN_MAX_AGE = int(os.environ.get("PASSWORD_RESET_TOKEN_MAX_AGE", "3600"))

    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.gmail.com")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD")
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"


class DevelopmentConfig(Config):
    DEBUG = os.environ.get("FLASK_DEBUG", "true").lower() == "true"


class TestingConfig(Config):
    TESTING = True
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    SECRET_KEY = "test-secret-key-with-at-least-32-bytes"
    JWT_SECRET_KEY = "test-jwt-secret-key-with-at-least-32-bytes"


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
}
