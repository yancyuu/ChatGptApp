# -*- coding: utf-8 -*-

from controller.controller_base import ControllerBase
from common_sdk.data_transform import protobuf_transformer
from manager.common_manager import CommonManager
from dao.common_da_helper import CommonDAHelper


class CommonController(ControllerBase):

    @property
    def manager(self):
        return self._manager

    def __init__(self, request, db, coll, pb):
        super().__init__(request)
        self._da = CommonDAHelper(db, coll)
        self._manager = CommonManager(self.user_id, self._da)
        self._OP_FUNC_MAP = {'create': self.create, 'update': self.update, 'get': self.get, 'list': self.list, 'delete': self.delete}
        self._pb = pb

    def create(self):
        template = protobuf_transformer.dict_to_protobuf(self.request.json, self._pb)
        template = self._manager.create(template)
        return protobuf_transformer.protobuf_to_dict(template)

    def update(self):
        template = protobuf_transformer.dict_to_protobuf(self.request.json, self._pb)
        template = self._manager.update(template)
        return protobuf_transformer.protobuf_to_dict(template)

    def get(self):
        id = self.get_json_param('id')
        template = self._manager.get(id)
        return protobuf_transformer.protobuf_to_dict(self._da.parse_document(template, cls=self._pb))

    def list(self):
        id_list = self.get_json_param('idList')
        orderby = self.get_json_param("orderby")
        comparisons = self.get_json_param("comparisons")
        size = self.get_json_param("size")
        matcher = {}
        if id_list is not None:
            matcher.update({"id": {"$in": id_list}})

        for field, value in self.request.json.items():
            matcher.update({field: value})
        templates = self._manager.list(comparisons=comparisons, conditions=matcher)
        return protobuf_transformer.batch_protobuf_to_dict(self._da.parse_documents(templates, orderby=orderby, cls=self._pb, size=size))

    def delete(self):
        id = self.get_json_param('id')
        if not id:
            return 0
        return self._manager.delete(id)
