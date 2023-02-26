from manager.common_manager import CommonManager
from manager.api.openai.operate import Operate

'''
    微信小程序授权服务
'''


class OpenaiManager(CommonManager):
    # 两小时有效时间
    EXPIRATION_PERIOD = 3600 * 2
    MODEL = "MODEL"
    ENGINE = "ENGINE"

    @property
    def api(self):
        return self._api

    def __init__(self, dao_helper=None, user_id=None):
        super().__init__(da=dao_helper, user_id=user_id)
        self._api = Operate()
        self.customer_da_helper = dao_helper

    def make_completion(self, prompt):
        return self.api.completion(prompt, self.engine)

    def api_list(self, type):
        if type == self.ENGINE:
            return self.api.list_engine()
        return self.api.list_models()

    def edit(self, input, instruction):
        return self.api.edit(input, instruction, self.engine)
