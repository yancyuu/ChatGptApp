# -*- coding: utf-8 -*-

from manager.api_result import ApiResult as BaseApiResult
import proto.organization.customer_pb2 as customer_pb
from service import error_codes


class ApiResult(BaseApiResult):

    def __init__(self, result=None):
        self.__customer_type = customer_pb.Customer.Method.WECHAT
        self.__result = result
        self.__init()

    def __init(self):
        if self.__result is None:
            return
        if isinstance(self.__result, dict):
            self.__result_code = error_codes.SUCCESS[0]
            self.__result_msg = error_codes.SUCCESS[1]
        else:
            self.__result_code = error_codes.LOGIN_FAILED[0]
            self.__result_msg = self.__result
    @property
    def session_key(self):
        """获取微信的session"""
        return self.__result.get("session_key")

    @property
    def open_id(self):
        return self.__result.get("openid")

    @property
    def union_id(self):
        return self.__result.get("unionid")
