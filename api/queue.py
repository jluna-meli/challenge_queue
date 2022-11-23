from flask import Blueprint, request
from services import auth
from services import queue

routes_queue = Blueprint("queue", __name__)


@routes_queue.before_request
def verify_token_middleware():
    return auth.verify_token_service()


@routes_queue.route("/connection/ping", methods=["GET"])
def connection_redis():
    return auth.connection_redis_service()

@routes_queue.route("/count", methods=["GET"])
def count_messages_with_redis():
    return queue.count_messages_service()


@routes_queue.route("/push", methods=["POST"])
def create_r_redis():
    data = request.get_json()
    return queue.push_message_service(data)

@routes_queue.route("/pop", methods=["DELETE"])
def delete_r_redis():
    return queue.delete_mesaage_service()

