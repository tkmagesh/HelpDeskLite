from flask import Flask

from helpdesk_lite.config import Config
from helpdesk_lite.database import init_database
from helpdesk_lite.routes.dashboard import dashboard_bp
from helpdesk_lite.routes.issues import issues_bp
from helpdesk_lite.routes.users import users_bp


def create_app(config_object=Config):
    app = Flask(__name__)
    app.config.from_object(config_object)

    init_database(app)

    app.register_blueprint(dashboard_bp)
    app.register_blueprint(issues_bp)
    app.register_blueprint(users_bp)

    return app
