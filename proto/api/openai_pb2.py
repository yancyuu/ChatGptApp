# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: proto/api/openai.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x16proto/api/openai.proto\"\xd9\x01\n\x06Openai\x12\n\n\x02id\x18\x01 \x01(\t\x12\x0f\n\x07user_id\x18\x02 \x01(\t\x12\x1a\n\x04type\x18\x03 \x01(\x0e\x32\x0c.Openai.Type\x12%\n\x07request\x18\x04 \x03(\x0b\x32\x14.Openai.RequestEntry\x12\x13\n\x0b\x63reate_time\x18\x05 \x01(\x03\x12\x18\n\x07\x63hoices\x18\x06 \x03(\x0b\x32\x07.Choice\x1a.\n\x0cRequestEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\"\x10\n\x04Type\x12\x08\n\x04TEXT\x10\x00\"v\n\x06\x43hoice\x12%\n\x07message\x18\x01 \x03(\x0b\x32\x14.Choice.MessageEntry\x12\x15\n\rfinish_reason\x18\x03 \x01(\t\x1a.\n\x0cMessageEntry\x12\x0b\n\x03key\x18\x01 \x01(\t\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'proto.api.openai_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _OPENAI_REQUESTENTRY._options = None
  _OPENAI_REQUESTENTRY._serialized_options = b'8\001'
  _CHOICE_MESSAGEENTRY._options = None
  _CHOICE_MESSAGEENTRY._serialized_options = b'8\001'
  _OPENAI._serialized_start=27
  _OPENAI._serialized_end=244
  _OPENAI_REQUESTENTRY._serialized_start=180
  _OPENAI_REQUESTENTRY._serialized_end=226
  _OPENAI_TYPE._serialized_start=228
  _OPENAI_TYPE._serialized_end=244
  _CHOICE._serialized_start=246
  _CHOICE._serialized_end=364
  _CHOICE_MESSAGEENTRY._serialized_start=318
  _CHOICE_MESSAGEENTRY._serialized_end=364
# @@protoc_insertion_point(module_scope)
