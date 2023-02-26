# -*- coding: utf-8 -*-
from common_sdk.data_transform import protobuf_transformer
from common_sdk.util import date_utils
from dao.helper.mongodb_dao_helper import MongodbClientHelper


class CommonDAHelper(MongodbClientHelper):

    @property
    def _collection(self):
        return self.mongo_client[self._db][self._coll]

    def __init__(self, db, coll):
        super().__init__()
        self._db = db
        self._coll = coll

    def add_or_update(self, template):
        matcher = {"id": template.id}
        json_data = protobuf_transformer.protobuf_to_dict(template)
        json_data.update({'updateTime': date_utils.timestamp_second()})
        self._collection.update_one(matcher, {"$set": json_data}, upsert=True)

    def get(self, conditions=None):
        if not conditions:
            return
        return self._collection.find_one(conditions)

    def list(self, comparisons=None, matcher=None):
        if matcher is None:
            matcher = {}
        contrasts = self.combination_contrasts(comparisons=comparisons)
        for contrast in contrasts:
            matcher.update(contrast)
        return self._collection.find(matcher)

    def delete(self, id):
        result = self._collection.delete_one({'id': id})
        return result.deleted_count
