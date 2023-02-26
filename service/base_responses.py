# -*- coding: utf-8 -*-
from flask import jsonify

from service import error_codes


def jsonify_response(data=None, status_response=None):
    if data is None:
        data = {}
    if status_response is None:
        status_response = {
            "errcode": error_codes.SUCCESS[0],
            "errmsg": error_codes.SUCCESS[1]
        }
    else:
        status_response = {
            "errcode": status_response[0],
            "errmsg": status_response[1]
        }
    ret = {}
    if data:
        ret = {
            "data": data
        }
    ret.update(**status_response)
    return jsonify(ret)

def service_jsonify_response(data):
    ret = {}
    if "errcode" in data and "errmsg" in data:
        status_response = {
            "errcode": data.get("errcode"),
            "errmsg": data.get("errmsg")
        }
        del data["errcode"]
        del data["errmsg"]
        ret.update({
            "data": data
        })
        ret.update(**status_response)
        return jsonify(ret)
    else:
        return jsonify_response(data)

def get_from_request(request, key, default=None):
    val = default
    if request.json:
        val = request.json.get(key)
    if request.args:
        val = request.args.get(key)
    return val
