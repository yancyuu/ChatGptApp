# -*- coding: utf-8 -*-

""" 小程序操作相关的函数
"""

import base64
import json
from Crypto.Cipher import AES
from common_sdk.logging.logger import logger
from common_sdk.util.application_utils import get_secret
from flask import current_app
from manager.organization.wechat.api_result import ApiResult
from service import errors, error_codes
from wechatpy.client import WeChatClient


class Operate:

    def __init__(self, app_id):
        self._app_secret = get_secret(app_id)
        self._app_id = app_id
        self.api = WeChatClient(self._app_id, self._app_secret, session=None)
        logger.info(f"app_config:{self.app_id}, {self.secret}")

    @property
    def app_id(self):
        return self._app_id

    @property
    def secret(self):
        return self._app_secret

    @property
    def access_token(self):
        return self.api.access_token

    @property
    def token(self):
        return current_app.config['WECHAT_TOKEN']

    def wxa_code_to_session(self, js_code):
        try:
            rst = self.api.wxa.code_to_session(js_code)
        except Exception as e:
            rst = str(e)
        logger.info("微信小程序接口返回数据 {}".format(rst))
        return self.create_api_result(rst)

    def decrypt_data(self, encrypt_data, session_key, iv):
        """ 微信授权登录，解码用户信息（示例源码可以在微信开放平台-小程序/开放能力/开放数据校验与加密 获取）
        """
        session_key = base64.b64decode(session_key)
        encrypt_data = base64.b64decode(encrypt_data)
        iv = base64.b64decode(iv)
        cipher = AES.new(session_key, AES.MODE_CBC, iv)
        s = cipher.decrypt(encrypt_data)
        un_pad_bytes = s[:-ord(s[len(s) - 1:])]
        decrypted = json.loads(self.try_decode_bytes_to_utf8(un_pad_bytes))
        if 'watermark' not in decrypted:
            return decrypted
        if decrypted['watermark']['appid'] != self.app_id:
            raise errors.Error(err=error_codes.INVALID_BUFFER)
        return decrypted

    @staticmethod
    def try_decode_bytes_to_utf8(buffer):
        """尝试将字节流转为UTF-8编码格式，若尝试失败，
        则尝试先以ISO-8859-1格式解码，然后再转换成UTF-8文本。
        """
        try:
            return buffer.decode('utf-8')
        except UnicodeDecodeError:
            return bytearray(buffer, 'iso-8859-1').decode('utf-8')

    @staticmethod
    def try_convert_text_to_utf8(text):
        """尝试将文本从ISO-8859-1格式转为UTF-8编码格式，若尝试失败，则直接返回原始文本。
        """
        try:
            return bytearray(text, 'iso-8859-1').decode('utf-8')
        except UnicodeEncodeError:
            return text

    @staticmethod
    def create_api_result(result):
        ret = ApiResult(result)
        return ret
