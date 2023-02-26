# -*- coding: utf-8 -*-

"""
统一小程序鉴权的返回格式
"""


class ApiResult:

    @property
    def service_printer_type(self):
        return self.service_printer_type

    @property
    def result_code(self):
        return self.__result_code

    @property
    def result_msg(self):
        return self.__result_msg

    @property
    def is_success(self):
        return False

    @property
    def result(self):
        return self.__result

