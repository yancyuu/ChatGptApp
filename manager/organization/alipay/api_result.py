# -*- coding: utf-8 -*-

from manager.api_result import ApiResult as BaseApiResult
import proto.organization.customer_pb2 as customer_pb


class ApiResult(BaseApiResult):

    def __init__(self, result=None):
        self.__customer_type = customer_pb.Customer.Method.ALIPAY
        self.__result = result
        self.__init()

    def __init(self):
        if self.__result is None:
            return
        self.__result_code = self.__result.get("ret")
        self.__result_msg = self.__result.get("msg")

    @property
    def result_msg(self):
        return self.__result_msg


