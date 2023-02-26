from common_sdk.util import id_generator
from manager.common_manager import CommonManager
from manager.auth.auth_manager import auth_manager
from manager.organization.wechat.operate import Operate
import proto.organization.customer_pb2 as customer_pb
from service import errors, error_codes
import time
'''
    微信小程序授权服务
'''


class AppletsAuthManager(CommonManager):
    # 两小时有效时间
    EXPIRATION_PERIOD = 3600 * 2

    @property
    def auth_api(self):
        return self._auth_api

    def __init__(self, dao_helper=None, app_id=None, user_id=None):
        super().__init__(da=dao_helper, user_id=user_id)
        self._auth_api = Operate(app_id)
        self.customer_da_helper = dao_helper

    def wechat_mini_program_login(self, js_code):
        """ 不授权登录。无法获取用户的信息
                若用户已经存在，直接返回用户信息
                若用户不存在，创建用户
        """
        ret = self.auth_api.wxa_code_to_session(js_code)
        if ret.result_code == error_codes.LOGIN_FAILED[0]:
            raise errors.CustomMessageError(ret.result_msg)
        open_id = ret.open_id
        customer = self.customer_da_helper.get_customer_by_matcher({"wechatProfile.openid": open_id})
        if customer is not None:
            return self.create_auth_token(customer)
        customer = customer_pb.Customer()
        customer.wechat_profile.openid = open_id
        customer.id = id_generator.generate_common_id()
        customer.create_time = str(int(time.time()))
        customer.method = customer_pb.Customer.Method.WECHAT
        self.customer_da_helper.add_or_update(customer)
        return self.create_auth_token(customer)

    def wechat_mini_program_auth(self, js_code=None, encrypted_data=None, iv=None):
        """ 授权登录。 可获取用户信息
            若客户存在，获取最新的客户信息，并更新原有数据
            若客户不存在，获取客户信息，并用客户信息创建新用户
        """
        ret = self.auth_api.wxa_code_to_session(js_code)
        if ret.result_code == error_codes.LOGIN_FAILED[0]:
            raise errors.CustomMessageError(ret.result_msg)
        open_id = ret.open_id
        union_id = ret.union_id
        customer = self.customer_da_helper.get_customer_by_matcher({"wechatProfile.openid": open_id})
        if customer is not None:
            return self.create_auth_token(customer)
        session_key = ret.session_key
        self.auth_api.wxa_code_to_session(js_code)
        decrypt_data = self._auth_api.decrypt_data(encrypted_data, session_key, iv)
        if not customer:
            customer = customer_pb.Customer()
            customer.create_time = str(int(time.time()))
            customer.id = id_generator.generate_common_id()
        customer.nickname = decrypt_data['nickName']
        sex = decrypt_data['gender']
        if sex != 0:
            customer.sex = "男" if sex == "1" else "女"
        customer.sex = "未知"
        customer.city = decrypt_data['city']
        customer.province = decrypt_data['province']
        customer.country = decrypt_data['country']
        customer.avatar = decrypt_data['avatarUrl']
        customer.method = customer_pb.Customer.Method.WECHAT
        customer.update_time = str(int(time.time()))
        customer.wechat_profile.openid = open_id
        if union_id is not None:
            customer.wechat_profile.union_id = union_id
        self.customer_da_helper.add_or_update(customer)
        return auth_manager.create_auth_token(customer)

    def create_auth_token(self, customer):
        return auth_manager.create_auth_token(customer)
