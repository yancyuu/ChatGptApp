# -*- coding: utf-8 -*-

from common_sdk.util import id_generator, date_utils
from common_sdk.data_transform import protobuf_transformer
from manager.manager_base import ManagerBase


class CommonManager(ManagerBase):

    @property
    def engine(self):
        return self._engine

    @engine.setter
    def engine(self, engine):
        self._engine = engine

    @property
    def da(self):
        return self._da

    def __init__(self, user_id=None, da=None):
        super().__init__(user_id)
        self._engine = None
        self._da = da

    def create(self, object):
        tmp = protobuf_transformer.protobuf_to_dict(object)
        if not tmp.get('id'):
            object.id = id_generator.generate_common_id()
        if tmp.get('createTime') is not None:
            object.create_time = date_utils.timestamp_second()
        self.da.add_or_update(object)
        return object

    def update(self, object):
        self.da.add_or_update(object)
        return object

    def get(self, object_id=None, conditions=None):
        if conditions is None:
            conditions = {}
        if object_id:
            conditions.update({"id": object_id})
        return self.da.get(conditions=conditions)

    def list(self, comparisons=None, conditions=None):
        if conditions is None:
            conditions = {}
        templates = self.da.list(comparisons=comparisons, matcher=conditions)
        return templates

    def delete(self, id):
        return self.da.delete(id)
