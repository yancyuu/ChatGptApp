# -*- coding: utf-8 -*-

from flask import Blueprint
from flask import request

from controller.organization.customer_controller import CustomerController
from service.base_responses import jsonify_response

bp_name = "customer"
_customer = Blueprint(bp_name, bp_name, url_prefix="/customer")


@_customer.route("/<string:operation>", methods=["POST"])
def template(operation):
    controller = CustomerController(request)
    ret = controller.do_operation(operation=operation)
    if ret:
        return jsonify_response(ret)
    return jsonify_response()
