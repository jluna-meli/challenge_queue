from flask import Blueprint
from services import auth

routes_auth = Blueprint("routes_auth", __name__)


@routes_auth.route("/login", methods=["POST"])
def login():
    return auth.login()


@routes_auth.route("/verify/token")
def verify():
    return auth.verify()
