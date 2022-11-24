import pytest
from __init import create_app


@pytest.fixture
def app(monkeypatch):
    monkeypatch.setenv('USERNAME', 'Admin')
    monkeypatch.setenv('PASSWORD', '1234')
    monkeypatch.setenv('SECRET', 'ThisIsTheKey')
    flask_app = create_app()
    return flask_app


@pytest.fixture
def auth(mocker):
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9" \
            ".eyJ1c2VybmFtZSI6IkFkbWluIiwicGFzc3dvcmQiOiIxMjM0IiwiZXhwIjoxNjY4ODY4NTM3fQ.mnOWYbg_IdMdU" \
            "-o2OqMbQ8u9lEgBDGLX3XFTfrqdrQY "
    mocker.patch("api.auth.login", return_value=token)
    mocker.patch("api.queue.verify_token_middleware", return_value=True)
    return token


@pytest.fixture()
def verify_response_token():
    return {
        "exp": 1669402693,
        "password": "1234",
        "username": "Admin"
    }


@pytest.fixture()
def data_login():
    return {
        "username": "Admin",
        "password": "1234"
    }
