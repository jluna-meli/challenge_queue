import pytest
from app import create_app


# @pytest.fixture()
# def client(app):
#     return app.test_client()


@pytest.fixture
def login_env(monkeypatch):
    monkeypatch.setenv('USERNAME', 'Admin')
    monkeypatch.setenv('PASSWORD', '1234')
    monkeypatch.setenv('SECRET', 'ThisIsTheKey')


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv('USERNAME', 'Admin')
    monkeypatch.setenv('PASSWORD', '1234')
    monkeypatch.setenv('SECRET', 'ThisIsTheKey')
    flask_app = create_app()
    return flask_app
