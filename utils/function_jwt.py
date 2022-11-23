from jwt import encode, decode, exceptions
from os import getenv
from datetime import datetime, timedelta
from flask import  jsonify

def expire_data (days: int):
    now = datetime.now()
    newDate = now + timedelta(days)
    return newDate

def create_token(data: dict):
    token = encode(payload={**data,
                            "exp": expire_data(1)},
                   key=getenv("SECRET"),
                   algorithm="HS256")
    return token

def validate_token(token, output=False):
    try:
        if output:
            return decode(token, key=getenv("SECRET"), algorithms=["HS256"])
        decode(token, key=getenv("SECRET"), algorithms=["HS256"])
    except exceptions.DecodeError:
        response = jsonify({"error": "Invalid token"})
        response.status_code = 401
        return response
    except exceptions.ExpiredSignatureError:
        response = jsonify({"error": "Token Expired"})
        response.status_code = 401
        return response