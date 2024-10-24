# Sets up test environment

import pytest
from backend import create_app, db

@pytest.fixture(scope='module')
def test_db():
    # Flask app set up
    app = create_app()
    app.config['TESTING'] = True
    # testing uses in-memory db
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client_test(test_db):
    return test_db.test_client()

@pytest.fixture(scope='function')
def init_db():
    # initialize db
    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()

