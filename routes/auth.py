from flask import Blueprint, request, jsonify
from config.function_jwt import create_token, validate_token
from os import getenv

routes_auth = Blueprint("routes_auth", __name__)

@routes_auth.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json()
        if data['username'] == getenv("USERNAME"):
            return create_token(data)
        else:
            response = jsonify({"error": "User not found"})
            response.status_code = 401
            return response
    except:
        return jsonify({"status": "Internal Error"}), 501

@routes_auth.route("/verify/token")
def verify():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        return validate_token(token, output=True)
    except:
        return jsonify({"status": "Internal Error"}), 501

