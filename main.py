from flask import Flask
from routes.auth import routes_auth
from routes.queue import routes_queue
from dotenv import load_dotenv

app = Flask(__name__)

app.register_blueprint(routes_auth, url_prefix="/api")
app.register_blueprint(routes_queue, url_prefix="/api/queue")


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    load_dotenv()
    app.run(debug=True, port="4000", host="0.0.0.0")

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
