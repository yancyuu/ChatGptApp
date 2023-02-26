# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from controller.identity.auth_token_controller import AuthTokenController
from service.base_responses import jsonify_response

bp_name = "auth_token"
_auth_token = Blueprint(bp_name, bp_name, url_prefix="/auth_token")


@_auth_token.route("/<string:operation>", methods=["POST"])
def template(operation):
    controller = AuthTokenController(request)
    ret = controller.do_operation(operation=operation)
    if ret:
        return jsonify_response(ret)
    return jsonify_response()
