import os

import fakeredis

import api.auth
import services.auth

try:
    import pytest
    import redis
    import tests.redis_tests.mocked_variables as mv
    import requests
except Exception as e:
    print("Some Modules are  Missing {} ".format(e))

# r = redis.Redis(host="redis-container", port=6379, db=0)
r = fakeredis.FakeStrictRedis(version=6)


@pytest.mark.parametrize("json, status_code, message",
                         [(mv.msg_success, 201, b'{"status":"success"}\n'),
                          (mv.msg_non_string, 400, b'{"error":"The message should be a string "}\n'),
                          (mv.msg_null, 400, b'{"error":"Message cannot be a null"}\n')])
def test_0_r_push_successful(app, mocker, client, json, status_code, message, auth):
    """
    Test when push a message successful
    """
    token = auth
    mocker.patch("services.queue.push_redis", return_value=1)

    # token = jwt_login(client)
    os.getenv("SECRET")
    response = client.post("/queue/push", json=json, headers={"Authorization": f"Bearer {token.encode()}"})
    assert response.status_code == status_code
    assert response.get_data() == message


def test_3__r_count(auth, mocker, client):
    """
    Test count the number of messages
    """
    token = auth
    mocker.patch("services.queue.counter_messages", return_value=1)

    response = client.get("/queue/count", headers={"Authorization": f"Bearer {token.encode()}"})
    assert response.status_code == 200
    # assert response.content == b'{\n  "count": '+ str(r.llen(('Messages'))).encode()+b',\n  "status": "0k"\n}\n'


@pytest.mark.parametrize("size, status_code, message", [(1, 200, b'{"msg":"' + str(r.lindex('Messages', 0)).encode() +
                                                         b'","status":"success"}\n'),
                                                        (0, 400, b'{"error":"Its not possible to delete any message '
                                                                 b'because there not messages in queue"}\n')])
def test_4_r_pop(auth, mocker, client, size, status_code, message):
    """
    Test Pop one message
    """
    token = auth
    mocker.patch("services.queue.counter_messages", return_value=size)
    mocker.patch("services.queue.msg_delete", return_value="None")
    mocker.patch("services.queue.delete_messages_redis", return_value=None)

    os.getenv("SECRET")
    response = client.delete("/queue/pop", headers={"Authorization": f"Bearer {token.encode()}"})
    assert response.status_code == status_code
    assert response.get_data() == message


def test_6_validate_token(mocker, client, auth, verify_response_token):
    token = auth

    mocker.patch("services.auth.verify", return_value=verify_response_token)

    response = client.get("/api/verify/token", headers={"Authorization": f"Bearer {token.encode()}"})
    assert response.status_code == 200
    assert response.get_data() == b'{"exp":1669402693,"password":"1234","username":"Admin"}\n'


def test_jwt_login(client, data_login):
    """
    Creating a jwt token
    """
    response = client.post("http://localhost:8000/api/login", json=data_login)
    assert response.status_code == 200


def create_one_message(client, auth):
    """
    Creating at least one message
    """
    token = auth
    response = client.post(mv.URL_QUEUE + "push", json=mv.msg_success,
                           headers={"Authorization": f"Bearer {token.encode()}"})
    print("this is ")
    print(response)
    return response


def test_delete_all_messsges():
    """
    Delete all messages
    """
    while r.llen('Messages') != 0:
        r.lpop('Messages')


if __name__ == "__main__":
    pytest.main()
