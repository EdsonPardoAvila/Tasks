from flask import Flask

from app.config import config
from app.extensions import db, migrate


def create_app(config_name=None):
    if config_name is None:
        config_name = "development"

    app = Flask(__name__, template_folder="views", static_folder="views/static")
    app.config.from_object(config[config_name])

    db.init_app(app)
    migrate.init_app(app, db)

    from app.controllers import calendar, main, user

    app.register_blueprint(main.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(calendar.bp)

    with app.app_context():
        db.create_all()

    return app
