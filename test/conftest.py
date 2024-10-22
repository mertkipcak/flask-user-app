import sys
import os
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from userbase import create_app
from userbase.utils.db import db

@pytest.fixture(scope='module')
def test_app():
    # Create the Flask app instance
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
        "JWT_SECRET_KEY": "test-secret"
    })

    # Initialize the database and create tables
    with app.app_context():
        db.create_all()

    yield app  # Run the tests

    # Clean up after tests
    with app.app_context():
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope='module')
def client(test_app):
    # Provide a test client for the app
    return test_app.test_client()
