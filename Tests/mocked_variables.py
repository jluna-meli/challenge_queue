import pytest

msg_success = {"msg": "This message"}
msg_non_string = {"msg": 15}
msg_null = {"msg": None}

data_login = {
    "username": "Admin",
    "password": "1234"
}

URL_LOGING_TEST = "http://localhost:8000/api/login"
URL_TOKEN_TEST = 'http://localhost:8000/api/verify/token'
URL_QUEUE = 'http://localhost:8000/queue/'
