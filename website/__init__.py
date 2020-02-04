from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.secret_key = "hellomynamestimandyouwontguessthis"
    db.init_app(app)
    app.config.from_object('config.Config')
    # APP ROUTES

    with app.app_context():
        # Imports
        from .views import view
        from .filters import filter
        from .models import Message

        app.register_blueprint(view, url_prefix="/")
        app.register_blueprint(filter, url_prefix="/filter")

        # Create tables for our models
        db.create_all()

        return app