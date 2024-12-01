from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_session import Session
from dotenv import load_dotenv
import os
from datetime import timedelta

db = SQLAlchemy()

load_dotenv()
secret_key = os.getenv("SECRET_KEY")

if not secret_key:
    raise RuntimeError(
        "SECRET_KEY is not set. Please set it in the environment variables."
    )


def create_app():
    app = Flask(__name__)
    CORS(app)

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Configure session
    app.config['SECRET_KEY'] = secret_key
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(days=7)
    app.config['SESSION_USE_SIGNER'] = True

    # Initialize session and database
    Session(app)
    db.init_app(app)

    # Import and register the blueprint
    from .routes import main
    app.register_blueprint(main)

    return app
