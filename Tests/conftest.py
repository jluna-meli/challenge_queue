import pytest
from main import app


@pytest.fixture()
def client():
    return app.test_client()


@pytest.fixture()
def login_env(monkeypatch):
    monkeypatch.setenv('USERNAME_TEST', 'Admin')
    monkeypatch.setenv('PASSWORD_TEST', '1234')


@pytest.fixture()
def url_env(monkeypatch):
    monkeypatch.setenv('URL_LOGING_TEST', 'http://localhost:8000/api/login')
    monkeypatch.setenv('URL_TOKEN_TEST', 'http://localhost:8000/api/verify/token')
    monkeypatch.setenv('URL_TEST', 'http://localhost:8000/api/queue/')

