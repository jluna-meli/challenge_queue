try:
    import pytest
    import tests.mocked_variables as mv
    import requests
    import json
except Exception as e:
    print("Some Modules are  Missing {} ".format(e))


def test_mega_integration():
    data = mv.data_login
    login = requests.post("http://localhost:8000/api/login", json=data)
    token = login.content.decode("utf-8")
    assert login.status_code == 200

    verify_token = requests.get("http://localhost:8000/api/verify/token", headers={"Authorization": f"Bearer {token}"})
    assert verify_token.status_code == 200
    assert json.loads(verify_token.content)["username"] == "Admin"
    assert json.loads(verify_token.content)["password"] == "1234"

    count = requests.get("http://localhost:8000/queue/count", headers={"Authorization": f"Bearer {token}"})
    current_count = json.loads(count.content.decode("utf-8"))["count"]
    assert count.status_code == 200
    assert json.loads(count.content)["status"] == '0k'
    assert json.loads(count.content)["count"] == current_count

    push = requests.post("http://localhost:8000/queue/push", json=mv.msg_success,
                         headers={"Authorization": f"Bearer {token}"})
    assert push.status_code == 201
    assert json.loads(push.content)["status"] == 'success'

    pop = requests.delete("http://localhost:8000/queue/pop", headers={"Authorization": f"Bearer {token}"})
    assert pop.status_code == 200
    assert json.loads(pop.content)["status"] == 'success'


if __name__ == "__main__":
    pytest.main()
