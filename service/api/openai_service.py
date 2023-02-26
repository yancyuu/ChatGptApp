# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from controller.api.openai_controller import OpenaiController
from service.base_responses import jsonify_response

bp_name = "openai"
_openai = Blueprint(bp_name, bp_name, url_prefix="/openai")


@_openai.route("/<string:operation>", methods=["POST"])
def template(operation):
    controller = OpenaiController(request)
    ret = controller.do_operation(operation=operation)
    if ret:
        return jsonify_response(ret)
    return jsonify_response()
