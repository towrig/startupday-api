"""Initialize Flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    """Construct the core application."""
    app = Flask(__name__, instance_relative_config=False)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/test.db'

    db.init_app(app)

    with app.app_context():
        from . import routes  # Import routes

        db.drop_all()
        db.create_all()  # Create database tables for our data models

        return app