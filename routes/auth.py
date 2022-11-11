from flask import Blueprint, request, jsonify
from config.function_jwt import create_token, validate_token

routes_auth = Blueprint("routes_auth", __name__)

@routes_auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if data['username'] == "Admin":
        return create_token(data)
    else:
        response = jsonify({"error": "User not found"})
        response.status_code = 401
        return response

@routes_auth.route("/verify/token")
def verify():
    token = request.headers['Authorization'].split(" ")[1]
    return validate_token(token, output=True)