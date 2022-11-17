
import redis
import werkzeug
from rq import Queue
from flask import Blueprint, jsonify, request, current_app
from werkzeug.exceptions import Unauthorized

from config.function_jwt import validate_token

routes_queue = Blueprint("queue", __name__)
@routes_queue.before_request
def verify_token_middleware():
    try:
        token = request.headers['Authorization'].split(" ")[1]
        return validate_token(token, output=False)
    except:
        return jsonify({"status": "Internal Error"}), 501


r = redis.Redis(host="redis-container",port=6379, db=0)
q = Queue(connection=r)

@routes_queue.route("/connection/ping", methods=["GET"] )
def connection_Redis():
    try:
        ping = "Connection successful" if r.ping() else "Ups, something happends with Redis Connection"

        response_object = {
            "status": ping,
        }
        return jsonify(response_object), 200 if r.ping() else 400
    except:
        return jsonify({"status": "Internal Error"}), 501


@routes_queue.route("/count", methods=["GET"] )
def count_messages_with_Redis():
    try:
        total = r.llen(('Messages'))
        response_object = {
            "status": "0k",
            "count": total
        }
        return jsonify(response_object), 200
    except:
        return jsonify({"status": "Internal Error"}), 501

@routes_queue.route("/push", methods=["POST"] )
def create_r_redis():
    try:
        if request.get_json()['msg'] == None:
            return jsonify({"error": "Message canot be a null"}), 400

        if isinstance(request.get_json()['msg'], str) == False:
            return jsonify({"error": "The message should be a string "}), 400
        r.lpush('Messages', request.get_json()['msg'])

        response_object = {
            "status": "success"
        }
        return jsonify(response_object), 201
    except:
        return jsonify({"status": "Internal Error"}), 501




@routes_queue.route("/pop", methods=["DELETE"] )
def delete_r_redis():
    try:
        if r.llen(('Messages')) == 0:
            return jsonify({"error": "Its not possible to delete any message because there not messages in queue"}), 400

        msg = r.lindex('Messages',0).decode()
        r.lpop('Messages')

        response_object = {
            "status": "success",
            "msg": msg
        }
        return jsonify(response_object), 200
    except:
        return jsonify({"status": "Internal Error"}), 501

