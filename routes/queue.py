import json
from time import strftime



import redis
from rq import Queue, Connection
from flask import Blueprint, jsonify, request, current_app

routes_queue = Blueprint("queue", __name__)


r = redis.Redis(host='localhost',port=6379,db=0)
q = Queue(connection=r)

@routes_queue.route("/push", methods=["POST"] )
def pop():

    data = request.get_json()
    message = data["msg"]
    job = r.mset({"msg": message})

    print(r.get("msg"))
    result = {
        "msg": message,
        "Time": strftime('%a, %d %b %Y %H:%M:%S')
    }
    return json.dumps({"result": result})


import time


def create_task(task_type):
    time.sleep(int(task_type) * 10)
    return True

@routes_queue.route("/push1", methods=["POST"] )
def run_task():
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
    return jsonify(response_object), 202

@routes_queue.route("/count", methods=["GET"] )
def count_messages():

    print(q.get_job_ids())
    print(q.get_jobs())
    response_object = {
        "status": "0k",
        "count": q.count
    }
    return jsonify(response_object), 202

@routes_queue.route("/count2", methods=["GET"] )
def count_messages_with_Redis():
    total = r.llen(('LanguageList'))
    response_object = {
        "status": "0k",
        "count": total
    }
    return jsonify(response_object), 202

@routes_queue.route("/push2", methods=["POST"] )
def create_r_queue():

    print(r.keys())
    r.lpush('LanguageList', request.get_json()['msg'])

    print(r.llen(('LanguageList')))
    l = r.lrange('LanguageList', 0,r.llen(('LanguageList'))-1)
    for x in l:
        print(x)

    # Elimina la lista
    #while (r.llen('LanguageList')!= 0):
    #    print(r.lpop('LanguageList'))
    response_object = {
        "status": "success"
    }
    return jsonify(response_object), 202

@routes_queue.route("/pop", methods=["DELETE"] )
def delete_r_queue():

    print(r.keys())
    msg = r.lindex('LanguageList',0).decode()
    r.lpop('LanguageList')

    print(r.llen(('LanguageList')))
    l = r.lrange('LanguageList', 0,r.llen(('LanguageList'))-1)
    for x in l:
        print(x)

    response_object = {
        "status": "success",
        "msg": msg
    }
    return jsonify(response_object), 202
