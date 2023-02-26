# -*- coding: utf-8 -*-

from abc import abstractmethod


class StorageInterface():

    @abstractmethod
    def save_token(self, token, key='id', expired=7200):
        ...

    @abstractmethod
    def check_token(self, token, key='id') -> bool:
        ...

    @abstractmethod
    def del_token(self, token, key='id') -> None:
        ...