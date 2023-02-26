# -*- coding: utf-8 -*-
from uuid import uuid4
from common_sdk.data_transform import protobuf_transformer
from common_sdk.auth.jwt_auth import jwt_auth
from manager.common_manager import CommonManager


class AuthManager(CommonManager):

    @staticmethod
    def create_auth_token(user):
        user = protobuf_transformer.protobuf_to_dict(user)
        data = {'id': user.get('id'), "exp": 0}
        token = jwt_auth.encode_token(data)
        decode_token = jwt_auth.decode_token(token)
        data.update({'refresh': str(uuid4()).replace('-', '')})
        user.update({'auth_token': token, 'refresh_token': jwt_auth.encode_token(data), 'expired': decode_token['exp']})
        return user


auth_manager = AuthManager()
