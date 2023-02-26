# -*- coding: utf-8 -*-

from manager.api_result import ApiResult as BaseApiResult
from service.errors import error_codes


class ApiResult(BaseApiResult):

    def __init__(self, result=None):
        self.__object = result.get("object")
        self.__result = result.get("data") if self.__object not in ["text_completion", "edit"] else result.get("choices")[0]
        self.__init()

    def __init(self):
        if self.__result is None:
            return
        self.__result_code = error_codes.SUCCESS[0] if self.__object else error_codes.API_FAILED[0]

    @property
    def result_msg(self):
        if self.__result_code != 0:
            return error_codes.API_FAILED[1]
        return error_codes.SUCCESS[1]
