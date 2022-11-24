import redis
from flask import jsonify

r = redis.Redis(host="redis-container", port=6379, db=0, socket_connect_timeout=2)


def connection_redis_service():
    try:
        ping = "Connection successful" if r.ping() else "Ups, something happends with Redis Connection"

        response_object = {
            "status": ping,
        }
        return jsonify(response_object), 200 if r.ping() else 400
    except:
        return jsonify({"status": "Internal Error"}), 501


def count_messages_service():
    try:
        total = counter_messages('Messages')
        response_object = {
            "status": "0k",
            "count": total
        }
        return jsonify(response_object), 200
    except:
        return jsonify({"status": "Internal Error"}), 501


def push_message_service(data):
    try:
        if data['msg'] is None:
            return jsonify({"error": "Message cannot be a null"}), 400

        if not isinstance(data['msg'], str):
            return jsonify({"error": "The message should be a string "}), 400

        push_redis('Messages', data['msg'])

        response_object = {
            "status": "success"
        }
        return jsonify(response_object), 201
    except:
        return jsonify({"status": "Internal Error"}), 501


def delete_mesaage_service():
    try:
        queue_size = counter_messages('Messages')
        if queue_size == 0:
            return jsonify({"error": "Its not possible to delete any message because there not messages in queue"}), 400

        msg = msg_delete('Messages', queue_size)
        delete_messages_redis('Messages')

        response_object = {
            "status": "success",
            "msg": msg
        }
        return jsonify(response_object), 200
    except:
        return jsonify({"status": "Internal Error"}), 501


def counter_messages(key):
    return r.llen(key)


def delete_messages_redis(key):
    return r.lpop(key)


def push_redis(key, value):
    return r.lpush(key, value)


def msg_delete(key, queue_size):
    return r.lindex(key, queue_size - 1).decode()
