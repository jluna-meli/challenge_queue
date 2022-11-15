import json
from time import strftime
import time
import redis
from rq import Queue
from flask import Blueprint, jsonify, request

routes_queue = Blueprint("queue", __name__)


r = redis.Redis(host="redis-container",port=6379, db=0)
q = Queue(connection=r)

@routes_queue.route("/push", methods=["POST"] )
def push_m_redis():

    data = request.get_json()
    message = data["msg"]
    job = r.mset({"msg": message})

    print(r.get("msg"))
    result = {
        "msg": job,
        "Time": strftime('%a, %d %b %Y %H:%M:%S')
    }
    return json.dumps({"result": result})


def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

@routes_queue.route("/push/enqueue", methods=["POST"] )
def create_message_with_enqueue():
    task_type = request.get_json()

    task = q.enqueue(create_task, task_type)
    print(q.get_job_ids())
    print(q.get_jobs())
    print(q.count)
    response_object = {
        "status": "success",
        "data": {
            "task_id": task.get_id()
        }
    }
    return jsonify(response_object), 201

@routes_queue.route("/count/enqueue", methods=["GET"] )
def count_messages_with_enqueue():

    print(q.get_job_ids())
    print(q.get_jobs())
    response_object = {
        "status": "0k",
        "count": q.count
    }
    return jsonify(response_object), 200

@routes_queue.route("/count2", methods=["GET"] )
def count_messages_with_Redis():
    total = r.llen(('Messages'))
    response_object = {
        "status": "0k",
        "count": total
    }
    return jsonify(response_object), 200

@routes_queue.route("/push2", methods=["POST"] )
def create_r_redis():

    print(r.keys())
    r.lpush('Messages', request.get_json()['msg'])

    print(r.llen(('Messages')))
    l = r.lrange('Messages', 0,r.llen(('Messages'))-1)
    for x in l:
        print(x)

    # Elimina la lista
    #while (r.llen('LanguageList')!= 0):
    #    print(r.lpop('LanguageList'))
    response_object = {
        "status": "success"
    }
    return jsonify(response_object), 200

@routes_queue.route("/pop", methods=["DELETE"] )
def delete_r_redis():

    print(r.keys())
    msg = r.lindex('Messages',0).decode()
    r.lpop('Messages')

    print(r.llen(('Messages')))
    l = r.lrange('Messages', 0,r.llen(('Messages'))-1)
    for x in l:
        print(x)

    response_object = {
        "status": "success",
        "msg": msg
    }
    return jsonify(response_object), 200
