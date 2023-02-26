# -*- coding: utf-8 -*-
from controller.common_controller import CommonController
from dao.constants import dao_constants
from manager.api.openai.openai_manager import OpenaiManager
from service.errors import CustomMessageError
import proto.api.openai_pb2 as openai_pb


class OpenaiController(CommonController):

    @property
    def manager(self):
        if not self._manager:
            self._manager = OpenaiManager(self._da, self.user_id)
            self._manager.engine = self.engine
        return self._manager

    def __init__(self, request):
        super().__init__(request, dao_constants.DB_API, dao_constants.COLL_OPENAI_NAME,
                         openai_pb.Openai)
        self._manager = None
        self._OP_FUNC_MAP = {
            'make_completion': self.make_completion,
            'api_list': self.api_list,
            'edit': self.edit,
        }

    def make_completion(self):
        prompt = self.get_json_param("prompt")
        if not prompt:
            raise CustomMessageError("未输入文本")
        res = self.manager.make_completion(prompt)
        if res.result_code != 0:
            raise CustomMessageError("请求失败")
        return res.result

    def api_list(self):
        type = self.get_json_param("type", self.manager.MODEL)
        res = self.manager.api_list(type)
        if res.result_code != 0:
            raise CustomMessageError("请求失败")
        return res.result

    def edit(self):
        input = self.get_json_param("input")
        instruction = self.get_json_param("instruction")
        res = self.manager.edit(input, instruction)
        if res.result_code != 0:
            raise CustomMessageError("请求失败")
        return res.result
