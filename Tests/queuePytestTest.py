try:
    import pytest
    import redis
    import Tests.mocked_variables as mv
except Exception as e:
    print("Some Modules are  Missing {} ".format(e))


r = redis.Redis(host="redis-container", port=6379, db=0)


@pytest.mark.parametrize("json, status_code, message",
                         [(mv.msg_success, 201, b'{\n  "status": "success"\n}\n'),
                          (mv.msg_non_string, 400, b'{\n  "error": "The message should be a string "\n}\n'),
                          (mv.msg_null, 400, b'{\n  "error": "Message canot be a null"\n}\n')])
def test_0_r_push_successful(client, mocker, json, status_code, message):
    """
    Test when push a message successful
    """

    # mocker.patch("routes.auth.login", return_value=None)
    mocker.patch("flask_jwt_extended.view_decorators.verify_jwt_in_request")
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6IkFkbWluIiwicGFzc3dvcmQiOiIxMjM0IiwiZXhwIjoxNjY4Njg4MDQxfQ.VopN8PDYImu-Mubp1JVOhS-4VFqg7LRZw_UCp_Qka3k"
    response = client.post(mv.URL_QUEUE + "push", json=json, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status_code
    assert response.content == message


def test_3__r_count(client):
    """
    Test count the number of messages
    """
    response = client.get(mv.URL_QUEUE + "count", headers={"Authorization": jwt_login(client)})
    assert response.status_code == 200
    # assert response.content == b'{\n  "count": '+ str(r.llen(('Messages'))).encode()+b',\n  "status": "0k"\n}\n'


# @pytest.mark.parametrize("status_code, message", [(200, b'{\n  "msg": "' + r.lindex('Messages', 0) +
#                                                    b'",\n  "status": "success"\n}\n'),
#                                                   (400, b'{\n  "error": "Its not possible to delete any message '
#                                                         b'because there not messages in queue"\n}\n ')])
# def test_4_r_pop(client, status_code, message):
#     """
#     Test Pop one message
#     """
#     # create_one_message(client)
#     response = client.delete(mv.URL_QUEUE + "pop", headers={"Authorization": jwt_login(client)})
#     assert response.status_code == status_code
#     assert response.content == message


@pytest.mark.parametrize("data, status_code",
                         [(mv.data_login, 200)])
def test_6_validate_token(client, data, status_code):
    token = "XFTfrqdrQY"

    response = client.get(mv.URL_TOKEN_TEST, json=data, headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == status_code


def jwt_login(client):
    """
    Creating a jwt token
    """
    # mocker.patch("routes.auth.login", return_value="eyjskdhfi")
    response = client.post(mv.URL_LOGING_TEST, json=mv.data_login)
    return response.get_data().decode()


def create_one_message(client):
    """
    Creating at least one message
    """
    client.post(mv.URL_QUEUE + "push", json=mv.msg_success, headers={"Authorization": jwt_login()})


def test_delete_all_messsges():
    """
    Delete all messages
    """
    while r.llen('Messages') != 0:
        r.lpop('Messages')


if __name__ == "__main__":
    pytest.main()
