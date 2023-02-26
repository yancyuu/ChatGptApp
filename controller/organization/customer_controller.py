import random
import hashlib
from controller.common_controller import CommonController
from common_sdk.data_transform import protobuf_transformer
from dao.constants import dao_constants
from manager.organization.customer_manager import CustomerManager
import proto.organization.customer_pb2 as customer_pb
from service import errors


class CustomerController(CommonController):
    PASSWORD_SALT = b"yancy"

    @property
    def manager(self):
        return self._manager

    def __init__(self, request):
        super().__init__(request, dao_constants.DB_ORGANIZATION_NAME, dao_constants.COLL_CUSTOMER_NAME,
                         customer_pb.Customer)
        self._manager = CustomerManager(user_id=self.user_id)
        self._OP_FUNC_MAP = {
            "get": self.get,
            "update": self.update,
            "get_customer_payment_info": self.get_customer_payment_info,
            "wechat_mini_program_login": self.wechat_mini_program_login,
            "wechat_mini_program_auth": self.wechat_mini_program_auth,
            "login_by_refresh_token": self.login_by_refresh_token,
            "login_by_password": self.login_by_password,
            "rejester": self.rejester,
        }

    def login_by_password(self):
        password = self.get_json_param("password")
        md = hashlib.md5(self.PASSWORD_SALT)
        md.update(password.encode("utf8"))
        password = md.hexdigest()
        matcher = {"phone": self.get_json_param("phone"), "password": password}
        object = protobuf_transformer.dict_to_protobuf(self.manager.get(conditions=matcher), self._pb)
        print(f"object  {object}")
        if not object:
            raise errors.CustomMessageError("用户或者密码错误")
        object.password = password
        return self.manager.create_auth_token(object)

    def rejester(self):
        """注册 todo: 不开放"""
        alphabet = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()'
        password = "".join(random.sample(alphabet, 8))
        object = protobuf_transformer.dict_to_protobuf(self.request.json, self._pb)
        customer = self.manager.get(conditions={"phone": object.phone})
        if customer:
            raise errors.CustomMessageError("用户已经存在")
        md = hashlib.md5(self.PASSWORD_SALT)
        md.update(password.encode("utf8"))
        object.password = md.hexdigest()
        self.manager.create(object)
        return {"id": object.id, "phone": object.phone, "password": password}

    def reset_password(self):
        # alphabet = 'abcdefghijklmnopqrstuvwxyz!@#$%^&*()'
        # password = random.sample(alphabet, 8)
        password = self.get_json_param('password')
        phone = self.get_json_param('phone')
        customer = protobuf_transformer.dict_to_protobuf(self.manager.get({"phone": phone}), self._pb)
        if not customer:
            raise errors.CustomMessageError("用户不存在")
        md = hashlib.md5(self.PASSWORD_SALT)
        md.update(password.encode("utf8"))
        password = md.hexdigest()
        customer.password = password
        customer = self.manager.update(customer)
        return {"id": customer.id, "phone": customer.phone, "password": customer.password}

    def wechat_mini_program_login(self):
        """ 微信小程序不授权个人信息登录
        """
        app_id = self.get_json_param("appId")
        code = self.get_json_param("code")
        return CustomerManager(app_id=app_id).wechat_mini_program_login(code)

    def wechat_mini_program_auth(self):
        """ 微信小程序授权登录
        """
        code = self.get_json_param("code")
        app_id = self.get_json_param("appId")
        iv = self.get_json_param("iv")
        encrypted_data = self.get_json_param("encryptedData")
        if not code or not app_id or not iv or not encrypted_data:
            raise errors.CustomMessageError("缺少参数")
        return CustomerManager(app_id=app_id).wechat_mini_program_auth(code, encrypted_data, iv)

    def get_customer_payment_info(self):
        """ 支付接口 通过token换取用户的第三方平台id
        """
        iam_token = self.get_json_param("token")
        customer = self.manager.get(iam_token)
        wechat_id = customer.wechat_profile.openid
        alipay_id = customer.alipay_profile.user_id
        payment_info = {"wechat": {"openid": wechat_id}, "alipay": {"userid": alipay_id}}
        return payment_info

    def login_by_refresh_token(self):
        token = self.get_json_param('token')
        return self._manager.login_by_refresh_token(token)
