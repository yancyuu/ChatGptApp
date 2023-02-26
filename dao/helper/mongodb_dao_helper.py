# -*- coding: utf-8 -*-

import os
from datetime import datetime

from google.protobuf import json_format

from pymongo import MongoClient

from common_sdk.base_class.singleton import SingletonMetaThreadSafe as SingletonMetaclass
from common_sdk.logging.logger import logger


class SingletonMongodbClientHelper(metaclass=SingletonMetaclass):

    def __init__(self):
        host = os.environ.get("MONGODB_ADDRESS")
        port = int(os.environ.get("MONGODB_PORT"))
        username = os.environ.get("MONGODB_USER_NAME")
        password = os.environ.get("MONGODB_ROOT_PASSWORD")
        replica_set = os.environ.get("MONGODB_REPLICA_SET")
        min_pool_size = os.environ.get("MONGODB_MIN_POOL_SIZE", 32)
        max_pool_size = os.environ.get("MONGODB_MAX_POOL_SIZE", 4096)
        replica_set_number = os.environ.get("MONGODB_REPLICA_SET_NUMBER", 1)
        logger.info(f"mongodb_config: {host}, {port}, {username}, {password}")
        if replica_set_number:
            self.mongo_client = MongoClient(host=host,
                                            port=port,
                                            username=username,
                                            password=password,
                                            replicaSet=replica_set,
                                            minPoolSize=min_pool_size,
                                            maxPoolSize=max_pool_size,
                                            w=replica_set_number,
                                            readPreference="secondaryPreferred")
        else:
            self.mongo_client = MongoClient(host=host,
                                            port=port,
                                            username=username,
                                            password=password,
                                            replicaSet=replica_set,
                                            minPoolSize=min_pool_size,
                                            maxPoolSize=max_pool_size)


class MongodbClientHelper():

    mongo_client = SingletonMongodbClientHelper().mongo_client

    def __init__(self, *args, **kargs):
        self._maximum_documents = 10000

    def limit_documents(self, cursor, orderby=None, page=None, size=None):
        if orderby is not None:
            cursor.sort(orderby)
        skip = None
        limit = size
        if size is None:
            limit = self._maximum_documents
        if page is not None and size is not None:
            skip = (page - 1) * size
        if skip is not None:
            return cursor.skip(skip).limit(limit)
        else:
            return cursor.limit(limit)

    def parse_documents(self, cursor, cls, orderby=None, page=None, size=None):
        cursor = self.limit_documents(cursor, orderby=orderby, page=page, size=size)
        ret = []
        for data in cursor:
            ret.append(self.parse_document(data, cls))
        return ret

    def parse_document(self, data, cls):
        if data is None:
            return None
        return json_format.ParseDict(data, cls(), ignore_unknown_fields=True)

    def combination_contrasts(self, comparisons=None):
        if comparisons is None:
            return []
        contrasts = []
        for comparison in comparisons:
            contrast = {}
            key = comparison.get("key")
            value = comparison.get("value")
            bigger = comparison.get("bigger", False)
            if None in (key, value, bigger):
                continue
            c = "$gt" if bigger else "$lt"
            contrast.update({key: {c: value}})
            contrasts.append(contrast)
        return contrasts
