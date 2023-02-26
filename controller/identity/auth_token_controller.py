# -*- coding: utf-8 -*-
from common_sdk.data_transform import protobuf_transformer
from controller.common_controller import CommonController
from dao.constants import dao_constants
from manager.identity.auth_token_manager import AuthTokenManager
import proto.identity.authentication_pb2 as authentication_pb

class AuthTokenController(CommonController):

    @property
    def manager(self):
        return self._manager

    def __init__(self, request):
        super().__init__(request, dao_constants.DB_IDENTITY_NAME, dao_constants.COLL_AUTH_TOKEN_NAME,
                         authentication_pb.AuthToken)
        self._manager = AuthTokenManager(self.user_id)
        self._OP_FUNC_MAP = {
            # AuthToken仅由内部产生，不支持外部API创建
            'refresh': self.refresh,
            'get': self.get,
            'list': self.list,
        }

    def refresh(self):
        user_id = self.get_json_param('user_id')
        iam_token = self.get_json_param('iam_token')
        auth_token = self.manager.refresh(user_id, iam_token)
        return protobuf_transformer.protobuf_to_dict(auth_token)

    def get(self):
        user_id = self.get_json_param('user_id')
        auth_token = self.manager.get(conditions={"userId": user_id})
        return protobuf_transformer.protobuf_to_dict(auth_token)
