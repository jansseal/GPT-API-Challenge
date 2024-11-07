# sets up test environment


import sys
import os

# Add the project root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend import create_app, db
import pytest


@pytest.fixture(scope='module')
def test_app():
    # Set up Flask app
    app = create_app()
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'  # In-memory database for testing
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Set up app context for the entire module
    with app.app_context():
        yield app


@pytest.fixture(scope='module')
def test_client(test_app):
    # Use the test client provided by Flask for API endpoint testing
    return test_app.test_client()


@pytest.fixture(scope='function')
def init_db(test_app):
    # Create all tables before each test function and drop them afterward
    with test_app.app_context():
        db.create_all()  # Initialize the database tables

        yield db  # Provide a clean database for each test

        db.session.remove()
        db.drop_all()  # Drop all tables after each test
