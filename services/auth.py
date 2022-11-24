import redis
from utils.function_jwt import create_token, validate_token
from flask import jsonify, request
from os import getenv

r = redis.Redis(host="redis-container", port=6379, db=0, socket_connect_timeout=2)


def verify_token_service():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        validate_token(token, output=False)

    except:
        return jsonify({"status": "Internal Error"}), 501


# def validate(token):
#     return validate_token(token, output=False)


def login():
    try:
        data = request.get_json()
        user = getenv("USERNAME")
        if data['username'] == user:
            return create_token(data)
        else:
            response = jsonify({"error": "User not found"})
            response.status_code = 401
            return response
    except Exception as e:
        return jsonify({"status": "Internal Error"}), 501


def connection_redis_service():
    try:
        ping = "Connection successful" if r.ping() else "Ups, something happends with Redis Connection"
        response_object = {
            "status": ping,
        }
        return jsonify(response_object), 200 if r.ping() else 400
    except:
        return jsonify({"status": "Internal Error"}), 501


def verify():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        return validate_token(token, output=True)
    except:
        return jsonify({"status": "Internal Error"}), 501
