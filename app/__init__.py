from flask import Flask

from config import Config
from app.extensions import csrf, db, login_manager, migrate
from app.models import Interaction, Lead, User
from app.routes import (
    api_routes,
    auth_routes,
    dashboard_routes,
    lead_routes,
    pipeline_routes,
    report_routes,
)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    csrf.init_app(app)

    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "warning"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    app.register_blueprint(auth_routes)
    app.register_blueprint(dashboard_routes)
    app.register_blueprint(lead_routes)
    app.register_blueprint(pipeline_routes)
    app.register_blueprint(report_routes)
    app.register_blueprint(api_routes, url_prefix="/api")

    return app
