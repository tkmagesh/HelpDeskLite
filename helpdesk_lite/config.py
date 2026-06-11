import os


class Config:
    SECRET_KEY = os.environ.get("HELPDESK_SECRET_KEY", "training-secret-key")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "HELPDESK_DATABASE_URL", "sqlite:///helpdesklite.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
