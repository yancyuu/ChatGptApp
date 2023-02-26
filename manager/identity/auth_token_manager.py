# -*- coding: utf-8 -*-
"""时来员工相关业务逻辑处理。"""

from common_sdk.util import date_utils
from common_sdk.util import id_generator
from dao.common_da_helper import CommonDAHelper
from dao.constants import dao_constants
from manager.common_manager import CommonManager
import proto.identity.authentication_pb2 as authentication_pb
from service import errors, error_codes
from manager.auth.auth_manager import AuthManager

# 两小时有效时间
EXPIRATION_PERIOD = 3600 * 2


class AuthTokenManager(CommonManager):

    def __init__(self, user_id=None):
        self._auth_token_da = CommonDAHelper(dao_constants.DB_IDENTITY_NAME, dao_constants.COLL_AUTH_TOKEN_NAME)
        super().__init__(user_id, self._auth_token_da)
        self._auth_manager = AuthManager()

    def create(self, user_id):
        token = authentication_pb.AuthToken()
        token.user_id = user_id
        token.token = id_generator.generate_common_id()
        token.create_time = date_utils.timestamp_second()
        token.expire_time = token.create_time + EXPIRATION_PERIOD
        self.da.add_or_update(token)
        return token

    def refresh(self, user_id, iam_token):
        token = self.get(user_id)
        if token.token != iam_token:
            raise errors.Error(err=error_codes.INVALID_TOKEN)
        return self.create(user_id)

    def create_auth_token(self, customer):
        return self._auth_manager.create_auth_token(customer)
