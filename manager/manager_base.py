# -*- coding: utf-8 -*-

import socket


class ManagerBase():
    """所有业务逻辑处理相关的ManagerBase基类。"""

    @property
    def user_id(self):
        return self._user_id

    @property
    def ip(self):
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        return ip

    def __init__(self, user_id=None):
        self._user_id = user_id
