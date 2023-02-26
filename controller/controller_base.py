# -*- coding: utf-8 -*-

from flask_httpauth import HTTPTokenAuth

from common_sdk.auth.jwt_auth import jwt_auth
from common_sdk.logging.logger import logger
from service import error_codes, errors


class ControllerBase(object):
    """所有支持API针对相应对象进行相关操作的Controller基类。"""
    auth = HTTPTokenAuth(scheme='Bearer')

    @property
    def request(self):
        return self._request

    @property
    def user_id(self):
        return self._user_id

    @property
    def engine(self):
        return self._engine


    @property
    def op_func_map(self):
        return self._OP_FUNC_MAP

    def __init__(self, request):
        self._request = request
        self._user_id = None
        self._engine = self.get_json_param("engine", "text-davinci-003")
        self._auth = self.check_token()
        # 从request操作类型(字符串)到相应处理函数的映射。
        self._OP_FUNC_MAP = {}

    def get_header_param(self, attr, default=None):
        return self.request.headers.get(attr, default)

    def get_json_param(self, attr, default=None):
        if not self.request.is_json:
            return default
        return self.request.json.get(attr, default)

    def check_token(self):
        try:
            auth = self.auth.get_auth()
            print(f"auth---->{auth}")
            if not auth:
                return False
            self._token = auth.get('token')
            if not jwt_auth.check_token(self._token):
                return False
            self._user_id = jwt_auth.get_token_data(self._token, 'id')
        except Exception as e:
            logger.error(e)
            return False
        return True

    def do_operation(self, operation):
        if not self._auth:
            raise errors.Error(error_codes.TOKEN_EXPIRED)
        if not self.check_permission(operation):
            raise PermissionError('Permission denied.')
        if operation not in self.op_func_map:
            raise NotImplementedError('Operation not implemented: {}'.format(operation))
        return self.op_func_map[operation]()

    def check_permission(self, operation, request_json=None):
        return True

    def __getattr__(self, key):
        if key in self.__dict__:
            return self.__dict__[key]
        return None
