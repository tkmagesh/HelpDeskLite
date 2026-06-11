from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def init_database(app):
    db.init_app(app)
    with app.app_context():
        db.create_all()


def reset_database():
    """Small helper used by tests and occasional classroom demos."""
    db.drop_all()
    db.create_all()
