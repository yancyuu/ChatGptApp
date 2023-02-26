from common_sdk.util import id_generator
from manager.organization.alipay.operate import Operate
from manager.auth.auth_manager import auth_manager
import proto.organization.customer_pb2 as customer_pb
import time

'''
    支付宝小程序授权服务
'''


class AlipayAuthManager:
    @property
    def auth_api(self):
        return self.auth_api

    def __init__(self, dao_helper=None, app_id=None):
        self._auth_api = Operate(app_id)
        self.customer_da_helper = dao_helper

    def alipay_mini_program_login(self, code):
        """ 支付宝小程序登录，只获取user_id
                若用户存在，则返回用户
                若用户不存在，则创建用户
        """
        ret = self._auth_api.get_access_token(code)
        if not ret:
            return
        user_id = ret.get("user_id")
        customer = self.customer_da_helper.get_customer_by_matcher({"alipayProfile.userId": user_id})
        if customer is not None:
            return self.create_auth_token(customer)
        customer = customer_pb.Customer()
        customer.alipay_profile.user_id = user_id
        customer.id = id_generator.generate_common_id()
        customer.create_time = str(int(time.time()))
        customer.method = customer_pb.Customer.Method.ALIPAY
        self.customer_da_helper.add_or_update_customer(customer)
        return self.create_auth_token(customer)

    def alipay_mini_program_auth(self, code, user_info):
        """ 支付宝小程序用户授权信息登录，用户信息由前端提供
        """
        ret = self._auth_api.get_access_token(code)
        if not ret:
            return
        user_id = ret.get("user_id")
        customer = self.customer_da_helper.get_customer_by_matcher({"alipayProfile.userId": user_id})
        if customer is None:
            customer = customer_pb.Customer()
            customer.id = id_generator.generate_common_id()
            customer.create_time = str(int(time.time()))
            customer.method = customer_pb.Customer.Method.ALIPAY
            customer.alipay_profile.user_id = user_id
        phone = user_info.get('phone')
        if phone is not None:
            customer.phone = phone
        sex = user_info.get('sex')
        if sex is not None:
            customer.sex = sex
        city = user_info.get('city')
        if city is not None:
            customer.city = city
        province = user_info.get('province')
        if province is not None:
            customer.province = province
        country = user_info.get('country')
        if country is not None:
            customer.country = country
        avatar = user_info.get('avatar')
        if avatar is not None:
            customer.avatar = avatar
        nickname = user_info.get('nickname')
        if nickname is not None:
            customer.nickname = nickname
        customer.update_time = str(int(time.time()))
        self.customer_da_helper.add_or_update_customer(customer)
        return self.create_auth_token(customer)

    def create_auth_token(self, customer):
        return auth_manager.create_auth_token(customer)
