# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: kvdb.proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()


import api_communication.proto.engine_pb2 as _engine_pb2
from google.protobuf import struct_pb2 as google_dot_protobuf_dot_struct__pb2


DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nkvdb.proto\x12\x19\x63om.xcyber360.api.engine.kvdb\x1a\x0c\x65ngine.proto\x1a\x1cgoogle/protobuf/struct.proto\"W\n\x05\x45ntry\x12\x10\n\x03key\x18\x01 \x01(\tH\x00\x88\x01\x01\x12*\n\x05value\x18\x02 \x01(\x0b\x32\x16.google.protobuf.ValueH\x01\x88\x01\x01\x42\x06\n\x04_keyB\x08\n\x06_value\"E\n\rdbGet_Request\x12\x11\n\x04name\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x10\n\x03key\x18\x02 \x01(\tH\x01\x88\x01\x01\x42\x07\n\x05_nameB\x06\n\x04_key\"\x98\x01\n\x0e\x64\x62Get_Response\x12\x32\n\x06status\x18\x01 \x01(\x0e\x32\".com.xcyber360.api.engine.ReturnStatus\x12\x12\n\x05\x65rror\x18\x02 \x01(\tH\x00\x88\x01\x01\x12*\n\x05value\x18\x03 \x01(\x0b\x32\x16.google.protobuf.ValueH\x01\x88\x01\x01\x42\x08\n\x06_errorB\x08\n\x06_value\"\x8c\x01\n\x10\x64\x62Search_Request\x12\x11\n\x04name\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x13\n\x06prefix\x18\x02 \x01(\tH\x01\x88\x01\x01\x12\x11\n\x04page\x18\x03 \x01(\rH\x02\x88\x01\x01\x12\x14\n\x07records\x18\x04 \x01(\rH\x03\x88\x01\x01\x42\x07\n\x05_nameB\t\n\x07_prefixB\x07\n\x05_pageB\n\n\x08_records\"\x98\x01\n\x11\x64\x62Search_Response\x12\x32\n\x06status\x18\x01 \x01(\x0e\x32\".com.xcyber360.api.engine.ReturnStatus\x12\x12\n\x05\x65rror\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x31\n\x07\x65ntries\x18\x03 \x03(\x0b\x32 .com.xcyber360.api.engine.kvdb.EntryB\x08\n\x06_error\"H\n\x10\x64\x62\x44\x65lete_Request\x12\x11\n\x04name\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x10\n\x03key\x18\x02 \x01(\tH\x01\x88\x01\x01\x42\x07\n\x05_nameB\x06\n\x04_key\"k\n\rdbPut_Request\x12\x11\n\x04name\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x34\n\x05\x65ntry\x18\x02 \x01(\x0b\x32 .com.xcyber360.api.engine.kvdb.EntryH\x01\x88\x01\x01\x42\x07\n\x05_nameB\x08\n\x06_entry\"\\\n\x12managerGet_Request\x12\x16\n\x0emust_be_loaded\x18\x01 \x01(\x08\x12\x1b\n\x0e\x66ilter_by_name\x18\x10 \x01(\tH\x00\x88\x01\x01\x42\x11\n\x0f_filter_by_name\"t\n\x13managerGet_Response\x12\x32\n\x06status\x18\x01 \x01(\x0e\x32\".com.xcyber360.api.engine.ReturnStatus\x12\x12\n\x05\x65rror\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x0b\n\x03\x64\x62s\x18\x03 \x03(\tB\x08\n\x06_error\"M\n\x13managerPost_Request\x12\x11\n\x04name\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x11\n\x04path\x18\x02 \x01(\tH\x01\x88\x01\x01\x42\x07\n\x05_nameB\x07\n\x05_path\"3\n\x15managerDelete_Request\x12\x11\n\x04name\x18\x01 \x01(\tH\x00\x88\x01\x01\x42\x07\n\x05_name\"o\n\x13managerDump_Request\x12\x11\n\x04name\x18\x01 \x01(\tH\x00\x88\x01\x01\x12\x11\n\x04page\x18\x02 \x01(\rH\x01\x88\x01\x01\x12\x14\n\x07records\x18\x03 \x01(\rH\x02\x88\x01\x01\x42\x07\n\x05_nameB\x07\n\x05_pageB\n\n\x08_records\"\x9b\x01\n\x14managerDump_Response\x12\x32\n\x06status\x18\x01 \x01(\x0e\x32\".com.xcyber360.api.engine.ReturnStatus\x12\x12\n\x05\x65rror\x18\x02 \x01(\tH\x00\x88\x01\x01\x12\x31\n\x07\x65ntries\x18\x03 \x03(\x0b\x32 .com.xcyber360.api.engine.kvdb.EntryB\x08\n\x06_errorb\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'kvdb_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ENTRY._serialized_start=85
  _ENTRY._serialized_end=172
  _DBGET_REQUEST._serialized_start=174
  _DBGET_REQUEST._serialized_end=243
  _DBGET_RESPONSE._serialized_start=246
  _DBGET_RESPONSE._serialized_end=398
  _DBSEARCH_REQUEST._serialized_start=401
  _DBSEARCH_REQUEST._serialized_end=541
  _DBSEARCH_RESPONSE._serialized_start=544
  _DBSEARCH_RESPONSE._serialized_end=696
  _DBDELETE_REQUEST._serialized_start=698
  _DBDELETE_REQUEST._serialized_end=770
  _DBPUT_REQUEST._serialized_start=772
  _DBPUT_REQUEST._serialized_end=879
  _MANAGERGET_REQUEST._serialized_start=881
  _MANAGERGET_REQUEST._serialized_end=973
  _MANAGERGET_RESPONSE._serialized_start=975
  _MANAGERGET_RESPONSE._serialized_end=1091
  _MANAGERPOST_REQUEST._serialized_start=1093
  _MANAGERPOST_REQUEST._serialized_end=1170
  _MANAGERDELETE_REQUEST._serialized_start=1172
  _MANAGERDELETE_REQUEST._serialized_end=1223
  _MANAGERDUMP_REQUEST._serialized_start=1225
  _MANAGERDUMP_REQUEST._serialized_end=1336
  _MANAGERDUMP_RESPONSE._serialized_start=1339
  _MANAGERDUMP_RESPONSE._serialized_end=1494
# @@protoc_insertion_point(module_scope)
