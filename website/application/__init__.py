from flask import Flask
from os import environ


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object('config.Config')
    app.secret_key = "no"

    # APP ROUTES

    with app.app_context():
        # Imports
        from .views import view
        from .filters import filter
        from .database import DataBase

        app.register_blueprint(view, url_prefix="/")
        app.register_blueprint(filter, url_prefix="/filter")

        return app