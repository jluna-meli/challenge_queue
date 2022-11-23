from flask import Flask
from api.auth import routes_auth
from api.queue import routes_queue


def create_app():
    app = Flask(__name__)

    app.register_blueprint(routes_auth, url_prefix="/api")
    app.register_blueprint(routes_queue, url_prefix="/queue")

    return app
