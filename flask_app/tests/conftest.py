import pytest
from src import create_app


@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
    })
    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username='test', password='test'):
        return self._client.post(
            '/login',
            json={'username': username, 'password': password}
        )


@pytest.fixture
def auth(client):
    return AuthActions(client)


# RUN:
# cd flask_tuto
# python -m pytest
