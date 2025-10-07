"""Application factory for the text viewer project."""

from typing import Optional

from flask import Flask

from .config import get_config
from .models import db


def create_app(config_name: Optional[str] = None) -> Flask:
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=False)
    config_class = get_config(config_name)
    app.config.from_object(config_class)
    app.config.from_prefixed_env()

    db.init_app(app)

    from .routes import bp as main_blueprint

    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    return app
