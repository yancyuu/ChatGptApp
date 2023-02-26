
from common_sdk.auth.jwt_auth import jwt_auth
from common_sdk.data_transform import protobuf_transformer
from dao.common_da_helper import CommonDAHelper
from dao.constants import dao_constants
from manager.organization.wechat.applets_auth_manager import AppletsAuthManager
import proto.organization.customer_pb2 as customer_pb


class CustomerManager(AppletsAuthManager):

    def __init__(self, app_id=None, user_id=None):
        super().__init__(
            dao_helper=CommonDAHelper(db=dao_constants.DB_ORGANIZATION_NAME, coll=dao_constants.COLL_CUSTOMER_NAME),
            app_id=app_id, user_id=user_id)

    def login_by_refresh_token(self, token):
        id = jwt_auth.get_token_data(token, 'id')
        customer = self.get(object_id=id)
        return self.create_auth_token(customer)

