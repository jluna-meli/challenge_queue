try:
    from main import app
    import unittest
    import requests
    import redis
    from Tests import factory
    from os import getenv

    from dotenv import load_dotenv

except Exception as e:
    print("Some Modules are  Missing {} ".format(e))

class QueueTest(unittest.TestCase):
    load_dotenv()
    URL_QUEUE= getenv("URL_TEST")
    URL_LOGIN = getenv("URL_LOGING_TEST")
    URL_TOKEN = getenv("URL_TOKEN_TEST")

    r = redis.Redis(host="localhost", port=6379, db=0)

    msg = factory.msg
    msg2 = factory.msg2
    msg3 = factory.msg3

    data = {"username": getenv("USERNAME_TEST"),"password": getenv("PASSWORD_TEST")}


    def test_0_r_push_successful(self):
        """
        Test when push a message successful
        """
        response = requests.post(self.URL_QUEUE + "push", json= self.msg, headers={"Authorization": self.jwt_login()})
        messageResponse = b'{\n  "status": "success"\n}\n'
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content, messageResponse)

    def test_1__r_push_fail_when_msg_is_not_string(self):
        """
        Test Push fail when msg is not a string
        """
        response = requests.post(self.URL_QUEUE + "push", json= self.msg2, headers={"Authorization": self.jwt_login()})
        message = b'{\n  "error": "The message should be a string "\n}\n'
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, message)

    def test_2__r_push_fail_when_msg_is_null(self):
        """
        Test Push fail when msg is null
        """
        response = requests.post(self.URL_QUEUE + "push", json= self.msg3, headers={"Authorization": self.jwt_login()})
        message = b'{\n  "error": "Message canot be a null"\n}\n'
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, message)

    def test_3__r_count(self):
        """
        Test count the number of messages
        """
        response = requests.get(self.URL_QUEUE + "count", headers={"Authorization": self.jwt_login()})
        message = b'{\n  "count": '+ str(self.r.llen(('Messages'))).encode()+b',\n  "status": "0k"\n}\n'

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, message)

    def test_4_r_pop(self):
        """
        Test Pop a message success
        """
        self.create_one_message()
        response = requests.delete(self.URL_QUEUE + "pop", headers={"Authorization": self.jwt_login()})
        message = b'{\n  "msg": "' + self.r.lindex('Messages',0)+ b'",\n  "status": "success"\n}\n'

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, message)

    def test_5_r_pop_fail(self):
        """
        Test Pop a message success
        """
        self.delete_all_messsges()
        response = requests.delete(self.URL_QUEUE + "pop", headers={"Authorization": self.jwt_login()})
        message = (b'{\n  "error": "Its not possible to delete any message because there not messages in queue"\n}\n')

        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.content, message)


    def test_6_validate_token(self):
        response = requests.get(self.URL_TOKEN, json=self.data, headers={"Authorization": self.jwt_login()})
        self.assertEqual(response.status_code, 200)

    def jwt_login(self):
        """
        Creating a jwt token
        """
        response = requests.post(self.URL_LOGIN, json=self.data)
        return "Bearer " + response.content.decode()

    def create_one_message(self):
        """
        Creating at least one message
        """

        print(self.r.llen('Messages'))
        requests.post(self.URL_QUEUE + "push", json=self.msg, headers={"Authorization": self.jwt_login()})


    def delete_all_messsges(self):
        """
        Delete all messages
        """
        while(self.r.llen('Messages')!= 0):
            self.r.lpop('Messages')


if __name__ == "__main__":
    unittest.main()