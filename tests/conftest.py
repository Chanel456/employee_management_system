import pytest

from app import create_app, db
from config.test_config import TestConfig

@pytest.fixture
def app():
    app = create_app(TestConfig)

    with app.app_context():
        db.create_all()

    yield app

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def runner(app):
    return app.test_cli_runner()

class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, email='test@test.com', password='test'):
        return self._client.post(
           '/login',
            data={'email': email, 'password': password}
        )

    def logout(self):
        return  self._client.get('/logout')

@pytest.fixture
def auth(client):
    return AuthActions(client)