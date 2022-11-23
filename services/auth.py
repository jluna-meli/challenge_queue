from utils.function_jwt import validate_token
from flask import jsonify, request


def verify_token_service():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        validate_token(token, output=False)

    except:
        return jsonify({"status": "Internal Error"}), 501


