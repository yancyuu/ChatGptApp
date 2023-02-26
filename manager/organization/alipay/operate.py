# -*- coding: utf-8 -*-

""" 支付宝操作相关的函数
"""
from base64 import encodebytes
from common_sdk.logging.logger import logger
from common_sdk.util.application_utils import get_secret
from datetime import datetime
import requests
from manager.organization.alipay.api_result import ApiResult
from urllib.parse import urlencode
from Cryptodome.Hash import SHA256 as CryptodomeSHA256
from Cryptodome.PublicKey import RSA as CryptodomeRSA
from Cryptodome.Signature import PKCS1_v1_5 as CryptodomePKCS1_v1_5


class Operate:

    def __init__(self, app_id):
        self._app_secret = get_secret(app_id)
        self._app_id = app_id
        self._alipay_api_url = "https://openapi.alipay.com/gateway.do"
        logger.info(f"print_config: {self.host}, {self.user}, {self.key}")

    @property
    def app_id(self):
        return self._app_id

    @property
    def private_key_string(self):
        return self._app_secret

    @property
    def alipay_api_url(self):
        return self._alipay_api_url

    def get_access_token(self, access_code):
        params = {
            "method": "alipay.system.oauth.token",
            "grant_type": "authorization_code",
            "code": access_code
        }
        url = self.alipay_api_url + "?charset=utf-8"
        return self.do_json_post(url=url, params=params)

    def get_user_share_info(self, auth_token):
        params = {
            "method": "alipay.user.info.share",
            "auth_token": auth_token
        }
        return self.do_json_get(url=self.alipay_api_url, params=params)

    def refresh_access_token(self, access_code, refresh_token):
        params = {
            "method": "alipay.system.oauth.token",
            "grant_type": "refresh_code",
            "code": access_code,
            "refresh_token": refresh_token
        }
        return self.do_json_get(url=self.alipay_api_url, params=params)

    def do_json_post(self, url, params, timeout=30, try_times=5):
        """ 以POST上送json数据
        """
        request_data = {
            "timestamp": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
            "app_id": self.app_id,
            "sign_type": "RSA2",
            "version": "1.0",
            "charset": "utf-8",
        }
        request_data.update(params)
        logger.info(f"支付宝请求接口: {url} {request_data}")
        # 生成签名
        self.add_sign_string(request_data)
        try:
            ret = requests.post(url, data=params, timeout=timeout)
            ret = ret.json()
            logger.info(f"支付宝请求接口返回: {ret}")
            return self.create_api_result(ret)
        except requests.RequestException as err:
            if try_times <= 0:
                raise err
            self.do_json_post(url, params, timeout=timeout, try_times=try_times - 1)

    def do_json_get(self, url, params, timeout=30, try_times=5):
        request_data = {
            "timestamp": datetime.strftime(datetime.now(), "%Y-%m-%d %H:%M:%S"),
            "app_id": self.app_id,
            "sign_type": "RSA2",
            "version": "1.0",
            "charset": "utf-8",
        }
        request_data.update(params)
        self.add_sign_string(request_data)
        request_string = urlencode(request_data)
        logger.info(f"支付宝请求接口: {url} {request_string}")
        try:
            url = f"{url}?{request_string}"
            ret = requests.get(url, timeout=timeout)
            ret = ret.json()
            logger.info(f"飞鹅请求接口返回: {ret}")
            return self.create_api_result(ret)
        except requests.RequestException as err:
            if try_times <= 0:
                raise err
            self.do_json_get(url, params, timeout=timeout, try_times=try_times - 1)

    def rsa2_sign(self, message):
        """使用rsa2签名"""
        signer = CryptodomePKCS1_v1_5.new(CryptodomeRSA.importKey(self.alipay_shilai_private_key_string))
        hash_value = CryptodomeSHA256.new(message)
        signature = signer.sign(hash_value)
        sign = encodebytes(signature).decode("utf8").replace("\n", "")
        return sign

    def add_sign_string(self, params):
        """
        将所有的请求参数按照"键=值&键=值"的格式，并rsa2加密后放到sign中
        """
        params.pop('sign', None)
        keys = params.keys()
        # 按照升序
        sorted_keys = sorted(keys, key=lambda x: x)
        keys = []
        for key in sorted_keys:
            value = params.get(key)
            if value == '':
                continue
            if isinstance(value, str):
                keys.append('{}={}'.format(key, value))
            elif isinstance(value, dict):
                keys.append('{}={}'.format(key, str(value)))
        s = '&'.join(keys)
        sign = self.rsa2_sign(s.encode(encoding='utf-8'))
        params['sign'] = sign

    @staticmethod
    def create_api_result(result):
        ret = ApiResult(result)
        return ret
