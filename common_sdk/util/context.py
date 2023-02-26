# -*- coding: utf-8 -*-

from contextvars import ContextVar

HTTP_MESSAGE_UUID = "message_id"
HTTP_REQUEST_TIMESTAMP = "request_timestamp"
COMMON_CONTEXT = 'context'

_message_id_ctx_var: ContextVar[str] = ContextVar(HTTP_MESSAGE_UUID, default=None)
_request_timestamp_ctx_var: ContextVar[int] = ContextVar(HTTP_REQUEST_TIMESTAMP, default=None)
_common_ctx_var: ContextVar[dict] = ContextVar(COMMON_CONTEXT, default={})


def get(key: str):
    return _common_ctx_var.get().get(key)


def set(key: str, val) -> None:
    _common_ctx_var.get().update({key: val})


def get_message_uuid() -> str:
    return _message_id_ctx_var.get()


def set_message_uuid(id: str) -> str:
    return _message_id_ctx_var.set(id)


def get_request_timestamp() -> int:
    return _request_timestamp_ctx_var.get()


def set_request_timestamp(timestamp: int) -> int:
    return _request_timestamp_ctx_var.set(timestamp)