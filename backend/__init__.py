from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .routes import main

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import and register routes here
    app.register_blueprint(main)

    return app
