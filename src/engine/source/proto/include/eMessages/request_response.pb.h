// Generated by the protocol buffer compiler.  DO NOT EDIT!
// source: request_response.proto

#ifndef GOOGLE_PROTOBUF_INCLUDED_request_5fresponse_2eproto
#define GOOGLE_PROTOBUF_INCLUDED_request_5fresponse_2eproto

#include <limits>
#include <string>

#include <google/protobuf/port_def.inc>
#if PROTOBUF_VERSION < 3021000
#error This file was generated by a newer version of protoc which is
#error incompatible with your Protocol Buffer headers. Please update
#error your headers.
#endif
#if 3021012 < PROTOBUF_MIN_PROTOC_VERSION
#error This file was generated by an older version of protoc which is
#error incompatible with your Protocol Buffer headers. Please
#error regenerate this file with a newer version of protoc.
#endif

#include <google/protobuf/port_undef.inc>
#include <google/protobuf/io/coded_stream.h>
#include <google/protobuf/arena.h>
#include <google/protobuf/arenastring.h>
#include <google/protobuf/generated_message_util.h>
#include <google/protobuf/metadata_lite.h>
#include <google/protobuf/generated_message_reflection.h>
#include <google/protobuf/message.h>
#include <google/protobuf/repeated_field.h>  // IWYU pragma: export
#include <google/protobuf/extension_set.h>  // IWYU pragma: export
#include <google/protobuf/unknown_field_set.h>
#include "engine.pb.h"
#include <google/protobuf/struct.pb.h>
// @@protoc_insertion_point(includes)
#include <google/protobuf/port_def.inc>
#define PROTOBUF_INTERNAL_EXPORT_request_5fresponse_2eproto
PROTOBUF_NAMESPACE_OPEN
namespace internal {
class AnyMetadata;
}  // namespace internal
PROTOBUF_NAMESPACE_CLOSE

// Internal implementation detail -- do not use these members.
struct TableStruct_request_5fresponse_2eproto {
  static const uint32_t offsets[];
};
extern const ::PROTOBUF_NAMESPACE_ID::internal::DescriptorTable descriptor_table_request_5fresponse_2eproto;
namespace com {
namespace xcyber360 {
namespace api {
namespace engine {
namespace test {
class Request;
struct RequestDefaultTypeInternal;
extern RequestDefaultTypeInternal _Request_default_instance_;
class Response;
struct ResponseDefaultTypeInternal;
extern ResponseDefaultTypeInternal _Response_default_instance_;
}  // namespace test
}  // namespace engine
}  // namespace api
}  // namespace xcyber360
}  // namespace com
PROTOBUF_NAMESPACE_OPEN
template<> ::com::xcyber360::api::engine::test::Request* Arena::CreateMaybeMessage<::com::xcyber360::api::engine::test::Request>(Arena*);
template<> ::com::xcyber360::api::engine::test::Response* Arena::CreateMaybeMessage<::com::xcyber360::api::engine::test::Response>(Arena*);
PROTOBUF_NAMESPACE_CLOSE
namespace com {
namespace xcyber360 {
namespace api {
namespace engine {
namespace test {

// ===================================================================

class Request final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:com.xcyber360.api.engine.test.Request) */ {
 public:
  inline Request() : Request(nullptr) {}
  ~Request() override;
  explicit PROTOBUF_CONSTEXPR Request(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  Request(const Request& from);
  Request(Request&& from) noexcept
    : Request() {
    *this = ::std::move(from);
  }

  inline Request& operator=(const Request& from) {
    CopyFrom(from);
    return *this;
  }
  inline Request& operator=(Request&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const Request& default_instance() {
    return *internal_default_instance();
  }
  static inline const Request* internal_default_instance() {
    return reinterpret_cast<const Request*>(
               &_Request_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    0;

  friend void swap(Request& a, Request& b) {
    a.Swap(&b);
  }
  inline void Swap(Request* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(Request* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  Request* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<Request>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const Request& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const Request& from) {
    Request::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(Request* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "com.xcyber360.api.engine.test.Request";
  }
  protected:
  explicit Request(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kDefaultStrFieldNumber = 1,
    kValueStringFieldNumber = 4,
    kAnyJSONFieldNumber = 5,
    kDefaultIntFieldNumber = 2,
    kDefaultBoolFieldNumber = 3,
  };
  // string defaultStr = 1;
  void clear_defaultstr();
  const std::string& defaultstr() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_defaultstr(ArgT0&& arg0, ArgT... args);
  std::string* mutable_defaultstr();
  PROTOBUF_NODISCARD std::string* release_defaultstr();
  void set_allocated_defaultstr(std::string* defaultstr);
  private:
  const std::string& _internal_defaultstr() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_defaultstr(const std::string& value);
  std::string* _internal_mutable_defaultstr();
  public:

  // optional string valueString = 4;
  bool has_valuestring() const;
  private:
  bool _internal_has_valuestring() const;
  public:
  void clear_valuestring();
  const std::string& valuestring() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_valuestring(ArgT0&& arg0, ArgT... args);
  std::string* mutable_valuestring();
  PROTOBUF_NODISCARD std::string* release_valuestring();
  void set_allocated_valuestring(std::string* valuestring);
  private:
  const std::string& _internal_valuestring() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_valuestring(const std::string& value);
  std::string* _internal_mutable_valuestring();
  public:

  // optional .google.protobuf.Value anyJSON = 5;
  bool has_anyjson() const;
  private:
  bool _internal_has_anyjson() const;
  public:
  void clear_anyjson();
  const ::PROTOBUF_NAMESPACE_ID::Value& anyjson() const;
  PROTOBUF_NODISCARD ::PROTOBUF_NAMESPACE_ID::Value* release_anyjson();
  ::PROTOBUF_NAMESPACE_ID::Value* mutable_anyjson();
  void set_allocated_anyjson(::PROTOBUF_NAMESPACE_ID::Value* anyjson);
  private:
  const ::PROTOBUF_NAMESPACE_ID::Value& _internal_anyjson() const;
  ::PROTOBUF_NAMESPACE_ID::Value* _internal_mutable_anyjson();
  public:
  void unsafe_arena_set_allocated_anyjson(
      ::PROTOBUF_NAMESPACE_ID::Value* anyjson);
  ::PROTOBUF_NAMESPACE_ID::Value* unsafe_arena_release_anyjson();

  // int32 defaultInt = 2;
  void clear_defaultint();
  int32_t defaultint() const;
  void set_defaultint(int32_t value);
  private:
  int32_t _internal_defaultint() const;
  void _internal_set_defaultint(int32_t value);
  public:

  // bool defaultBool = 3;
  void clear_defaultbool();
  bool defaultbool() const;
  void set_defaultbool(bool value);
  private:
  bool _internal_defaultbool() const;
  void _internal_set_defaultbool(bool value);
  public:

  // @@protoc_insertion_point(class_scope:com.xcyber360.api.engine.test.Request)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::internal::HasBits<1> _has_bits_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr defaultstr_;
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr valuestring_;
    ::PROTOBUF_NAMESPACE_ID::Value* anyjson_;
    int32_t defaultint_;
    bool defaultbool_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_request_5fresponse_2eproto;
};
// -------------------------------------------------------------------

class Response final :
    public ::PROTOBUF_NAMESPACE_ID::Message /* @@protoc_insertion_point(class_definition:com.xcyber360.api.engine.test.Response) */ {
 public:
  inline Response() : Response(nullptr) {}
  ~Response() override;
  explicit PROTOBUF_CONSTEXPR Response(::PROTOBUF_NAMESPACE_ID::internal::ConstantInitialized);

  Response(const Response& from);
  Response(Response&& from) noexcept
    : Response() {
    *this = ::std::move(from);
  }

  inline Response& operator=(const Response& from) {
    CopyFrom(from);
    return *this;
  }
  inline Response& operator=(Response&& from) noexcept {
    if (this == &from) return *this;
    if (GetOwningArena() == from.GetOwningArena()
  #ifdef PROTOBUF_FORCE_COPY_IN_MOVE
        && GetOwningArena() != nullptr
  #endif  // !PROTOBUF_FORCE_COPY_IN_MOVE
    ) {
      InternalSwap(&from);
    } else {
      CopyFrom(from);
    }
    return *this;
  }

  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* descriptor() {
    return GetDescriptor();
  }
  static const ::PROTOBUF_NAMESPACE_ID::Descriptor* GetDescriptor() {
    return default_instance().GetMetadata().descriptor;
  }
  static const ::PROTOBUF_NAMESPACE_ID::Reflection* GetReflection() {
    return default_instance().GetMetadata().reflection;
  }
  static const Response& default_instance() {
    return *internal_default_instance();
  }
  static inline const Response* internal_default_instance() {
    return reinterpret_cast<const Response*>(
               &_Response_default_instance_);
  }
  static constexpr int kIndexInFileMessages =
    1;

  friend void swap(Response& a, Response& b) {
    a.Swap(&b);
  }
  inline void Swap(Response* other) {
    if (other == this) return;
  #ifdef PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() != nullptr &&
        GetOwningArena() == other->GetOwningArena()) {
   #else  // PROTOBUF_FORCE_COPY_IN_SWAP
    if (GetOwningArena() == other->GetOwningArena()) {
  #endif  // !PROTOBUF_FORCE_COPY_IN_SWAP
      InternalSwap(other);
    } else {
      ::PROTOBUF_NAMESPACE_ID::internal::GenericSwap(this, other);
    }
  }
  void UnsafeArenaSwap(Response* other) {
    if (other == this) return;
    GOOGLE_DCHECK(GetOwningArena() == other->GetOwningArena());
    InternalSwap(other);
  }

  // implements Message ----------------------------------------------

  Response* New(::PROTOBUF_NAMESPACE_ID::Arena* arena = nullptr) const final {
    return CreateMaybeMessage<Response>(arena);
  }
  using ::PROTOBUF_NAMESPACE_ID::Message::CopyFrom;
  void CopyFrom(const Response& from);
  using ::PROTOBUF_NAMESPACE_ID::Message::MergeFrom;
  void MergeFrom( const Response& from) {
    Response::MergeImpl(*this, from);
  }
  private:
  static void MergeImpl(::PROTOBUF_NAMESPACE_ID::Message& to_msg, const ::PROTOBUF_NAMESPACE_ID::Message& from_msg);
  public:
  PROTOBUF_ATTRIBUTE_REINITIALIZES void Clear() final;
  bool IsInitialized() const final;

  size_t ByteSizeLong() const final;
  const char* _InternalParse(const char* ptr, ::PROTOBUF_NAMESPACE_ID::internal::ParseContext* ctx) final;
  uint8_t* _InternalSerialize(
      uint8_t* target, ::PROTOBUF_NAMESPACE_ID::io::EpsCopyOutputStream* stream) const final;
  int GetCachedSize() const final { return _impl_._cached_size_.Get(); }

  private:
  void SharedCtor(::PROTOBUF_NAMESPACE_ID::Arena* arena, bool is_message_owned);
  void SharedDtor();
  void SetCachedSize(int size) const final;
  void InternalSwap(Response* other);

  private:
  friend class ::PROTOBUF_NAMESPACE_ID::internal::AnyMetadata;
  static ::PROTOBUF_NAMESPACE_ID::StringPiece FullMessageName() {
    return "com.xcyber360.api.engine.test.Response";
  }
  protected:
  explicit Response(::PROTOBUF_NAMESPACE_ID::Arena* arena,
                       bool is_message_owned = false);
  public:

  static const ClassData _class_data_;
  const ::PROTOBUF_NAMESPACE_ID::Message::ClassData*GetClassData() const final;

  ::PROTOBUF_NAMESPACE_ID::Metadata GetMetadata() const final;

  // nested types ----------------------------------------------------

  // accessors -------------------------------------------------------

  enum : int {
    kErrorFieldNumber = 2,
    kValueStringFieldNumber = 4,
    kValueObjFieldNumber = 3,
    kStatusFieldNumber = 1,
  };
  // optional string error = 2;
  bool has_error() const;
  private:
  bool _internal_has_error() const;
  public:
  void clear_error();
  const std::string& error() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_error(ArgT0&& arg0, ArgT... args);
  std::string* mutable_error();
  PROTOBUF_NODISCARD std::string* release_error();
  void set_allocated_error(std::string* error);
  private:
  const std::string& _internal_error() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_error(const std::string& value);
  std::string* _internal_mutable_error();
  public:

  // optional string valueString = 4;
  bool has_valuestring() const;
  private:
  bool _internal_has_valuestring() const;
  public:
  void clear_valuestring();
  const std::string& valuestring() const;
  template <typename ArgT0 = const std::string&, typename... ArgT>
  void set_valuestring(ArgT0&& arg0, ArgT... args);
  std::string* mutable_valuestring();
  PROTOBUF_NODISCARD std::string* release_valuestring();
  void set_allocated_valuestring(std::string* valuestring);
  private:
  const std::string& _internal_valuestring() const;
  inline PROTOBUF_ALWAYS_INLINE void _internal_set_valuestring(const std::string& value);
  std::string* _internal_mutable_valuestring();
  public:

  // optional .google.protobuf.Value valueObj = 3;
  bool has_valueobj() const;
  private:
  bool _internal_has_valueobj() const;
  public:
  void clear_valueobj();
  const ::PROTOBUF_NAMESPACE_ID::Value& valueobj() const;
  PROTOBUF_NODISCARD ::PROTOBUF_NAMESPACE_ID::Value* release_valueobj();
  ::PROTOBUF_NAMESPACE_ID::Value* mutable_valueobj();
  void set_allocated_valueobj(::PROTOBUF_NAMESPACE_ID::Value* valueobj);
  private:
  const ::PROTOBUF_NAMESPACE_ID::Value& _internal_valueobj() const;
  ::PROTOBUF_NAMESPACE_ID::Value* _internal_mutable_valueobj();
  public:
  void unsafe_arena_set_allocated_valueobj(
      ::PROTOBUF_NAMESPACE_ID::Value* valueobj);
  ::PROTOBUF_NAMESPACE_ID::Value* unsafe_arena_release_valueobj();

  // .com.xcyber360.api.engine.ReturnStatus status = 1;
  void clear_status();
  ::com::xcyber360::api::engine::ReturnStatus status() const;
  void set_status(::com::xcyber360::api::engine::ReturnStatus value);
  private:
  ::com::xcyber360::api::engine::ReturnStatus _internal_status() const;
  void _internal_set_status(::com::xcyber360::api::engine::ReturnStatus value);
  public:

  // @@protoc_insertion_point(class_scope:com.xcyber360.api.engine.test.Response)
 private:
  class _Internal;

  template <typename T> friend class ::PROTOBUF_NAMESPACE_ID::Arena::InternalHelper;
  typedef void InternalArenaConstructable_;
  typedef void DestructorSkippable_;
  struct Impl_ {
    ::PROTOBUF_NAMESPACE_ID::internal::HasBits<1> _has_bits_;
    mutable ::PROTOBUF_NAMESPACE_ID::internal::CachedSize _cached_size_;
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr error_;
    ::PROTOBUF_NAMESPACE_ID::internal::ArenaStringPtr valuestring_;
    ::PROTOBUF_NAMESPACE_ID::Value* valueobj_;
    int status_;
  };
  union { Impl_ _impl_; };
  friend struct ::TableStruct_request_5fresponse_2eproto;
};
// ===================================================================


// ===================================================================

#ifdef __GNUC__
  #pragma GCC diagnostic push
  #pragma GCC diagnostic ignored "-Wstrict-aliasing"
#endif  // __GNUC__
// Request

// string defaultStr = 1;
inline void Request::clear_defaultstr() {
  _impl_.defaultstr_.ClearToEmpty();
}
inline const std::string& Request::defaultstr() const {
  // @@protoc_insertion_point(field_get:com.xcyber360.api.engine.test.Request.defaultStr)
  return _internal_defaultstr();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void Request::set_defaultstr(ArgT0&& arg0, ArgT... args) {
 
 _impl_.defaultstr_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:com.xcyber360.api.engine.test.Request.defaultStr)
}
inline std::string* Request::mutable_defaultstr() {
  std::string* _s = _internal_mutable_defaultstr();
  // @@protoc_insertion_point(field_mutable:com.xcyber360.api.engine.test.Request.defaultStr)
  return _s;
}
inline const std::string& Request::_internal_defaultstr() const {
  return _impl_.defaultstr_.Get();
}
inline void Request::_internal_set_defaultstr(const std::string& value) {
  
  _impl_.defaultstr_.Set(value, GetArenaForAllocation());
}
inline std::string* Request::_internal_mutable_defaultstr() {
  
  return _impl_.defaultstr_.Mutable(GetArenaForAllocation());
}
inline std::string* Request::release_defaultstr() {
  // @@protoc_insertion_point(field_release:com.xcyber360.api.engine.test.Request.defaultStr)
  return _impl_.defaultstr_.Release();
}
inline void Request::set_allocated_defaultstr(std::string* defaultstr) {
  if (defaultstr != nullptr) {
    
  } else {
    
  }
  _impl_.defaultstr_.SetAllocated(defaultstr, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.defaultstr_.IsDefault()) {
    _impl_.defaultstr_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:com.xcyber360.api.engine.test.Request.defaultStr)
}

// int32 defaultInt = 2;
inline void Request::clear_defaultint() {
  _impl_.defaultint_ = 0;
}
inline int32_t Request::_internal_defaultint() const {
  return _impl_.defaultint_;
}
inline int32_t Request::defaultint() const {
  // @@protoc_insertion_point(field_get:com.xcyber360.api.engine.test.Request.defaultInt)
  return _internal_defaultint();
}
inline void Request::_internal_set_defaultint(int32_t value) {
  
  _impl_.defaultint_ = value;
}
inline void Request::set_defaultint(int32_t value) {
  _internal_set_defaultint(value);
  // @@protoc_insertion_point(field_set:com.xcyber360.api.engine.test.Request.defaultInt)
}

// bool defaultBool = 3;
inline void Request::clear_defaultbool() {
  _impl_.defaultbool_ = false;
}
inline bool Request::_internal_defaultbool() const {
  return _impl_.defaultbool_;
}
inline bool Request::defaultbool() const {
  // @@protoc_insertion_point(field_get:com.xcyber360.api.engine.test.Request.defaultBool)
  return _internal_defaultbool();
}
inline void Request::_internal_set_defaultbool(bool value) {
  
  _impl_.defaultbool_ = value;
}
inline void Request::set_defaultbool(bool value) {
  _internal_set_defaultbool(value);
  // @@protoc_insertion_point(field_set:com.xcyber360.api.engine.test.Request.defaultBool)
}

// optional string valueString = 4;
inline bool Request::_internal_has_valuestring() const {
  bool value = (_impl_._has_bits_[0] & 0x00000001u) != 0;
  return value;
}
inline bool Request::has_valuestring() const {
  return _internal_has_valuestring();
}
inline void Request::clear_valuestring() {
  _impl_.valuestring_.ClearToEmpty();
  _impl_._has_bits_[0] &= ~0x00000001u;
}
inline const std::string& Request::valuestring() const {
  // @@protoc_insertion_point(field_get:com.xcyber360.api.engine.test.Request.valueString)
  return _internal_valuestring();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void Request::set_valuestring(ArgT0&& arg0, ArgT... args) {
 _impl_._has_bits_[0] |= 0x00000001u;
 _impl_.valuestring_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:com.xcyber360.api.engine.test.Request.valueString)
}
inline std::string* Request::mutable_valuestring() {
  std::string* _s = _internal_mutable_valuestring();
  // @@protoc_insertion_point(field_mutable:com.xcyber360.api.engine.test.Request.valueString)
  return _s;
}
inline const std::string& Request::_internal_valuestring() const {
  return _impl_.valuestring_.Get();
}
inline void Request::_internal_set_valuestring(const std::string& value) {
  _impl_._has_bits_[0] |= 0x00000001u;
  _impl_.valuestring_.Set(value, GetArenaForAllocation());
}
inline std::string* Request::_internal_mutable_valuestring() {
  _impl_._has_bits_[0] |= 0x00000001u;
  return _impl_.valuestring_.Mutable(GetArenaForAllocation());
}
inline std::string* Request::release_valuestring() {
  // @@protoc_insertion_point(field_release:com.xcyber360.api.engine.test.Request.valueString)
  if (!_internal_has_valuestring()) {
    return nullptr;
  }
  _impl_._has_bits_[0] &= ~0x00000001u;
  auto* p = _impl_.valuestring_.Release();
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.valuestring_.IsDefault()) {
    _impl_.valuestring_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  return p;
}
inline void Request::set_allocated_valuestring(std::string* valuestring) {
  if (valuestring != nullptr) {
    _impl_._has_bits_[0] |= 0x00000001u;
  } else {
    _impl_._has_bits_[0] &= ~0x00000001u;
  }
  _impl_.valuestring_.SetAllocated(valuestring, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.valuestring_.IsDefault()) {
    _impl_.valuestring_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:com.xcyber360.api.engine.test.Request.valueString)
}

// optional .google.protobuf.Value anyJSON = 5;
inline bool Request::_internal_has_anyjson() const {
  bool value = (_impl_._has_bits_[0] & 0x00000002u) != 0;
  PROTOBUF_ASSUME(!value || _impl_.anyjson_ != nullptr);
  return value;
}
inline bool Request::has_anyjson() const {
  return _internal_has_anyjson();
}
inline const ::PROTOBUF_NAMESPACE_ID::Value& Request::_internal_anyjson() const {
  const ::PROTOBUF_NAMESPACE_ID::Value* p = _impl_.anyjson_;
  return p != nullptr ? *p : reinterpret_cast<const ::PROTOBUF_NAMESPACE_ID::Value&>(
      ::PROTOBUF_NAMESPACE_ID::_Value_default_instance_);
}
inline const ::PROTOBUF_NAMESPACE_ID::Value& Request::anyjson() const {
  // @@protoc_insertion_point(field_get:com.xcyber360.api.engine.test.Request.anyJSON)
  return _internal_anyjson();
}
inline void Request::unsafe_arena_set_allocated_anyjson(
    ::PROTOBUF_NAMESPACE_ID::Value* anyjson) {
  if (GetArenaForAllocation() == nullptr) {
    delete reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.anyjson_);
  }
  _impl_.anyjson_ = anyjson;
  if (anyjson) {
    _impl_._has_bits_[0] |= 0x00000002u;
  } else {
    _impl_._has_bits_[0] &= ~0x00000002u;
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:com.xcyber360.api.engine.test.Request.anyJSON)
}
inline ::PROTOBUF_NAMESPACE_ID::Value* Request::release_anyjson() {
  _impl_._has_bits_[0] &= ~0x00000002u;
  ::PROTOBUF_NAMESPACE_ID::Value* temp = _impl_.anyjson_;
  _impl_.anyjson_ = nullptr;
#ifdef PROTOBUF_FORCE_COPY_IN_RELEASE
  auto* old =  reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(temp);
  temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  if (GetArenaForAllocation() == nullptr) { delete old; }
#else  // PROTOBUF_FORCE_COPY_IN_RELEASE
  if (GetArenaForAllocation() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
#endif  // !PROTOBUF_FORCE_COPY_IN_RELEASE
  return temp;
}
inline ::PROTOBUF_NAMESPACE_ID::Value* Request::unsafe_arena_release_anyjson() {
  // @@protoc_insertion_point(field_release:com.xcyber360.api.engine.test.Request.anyJSON)
  _impl_._has_bits_[0] &= ~0x00000002u;
  ::PROTOBUF_NAMESPACE_ID::Value* temp = _impl_.anyjson_;
  _impl_.anyjson_ = nullptr;
  return temp;
}
inline ::PROTOBUF_NAMESPACE_ID::Value* Request::_internal_mutable_anyjson() {
  _impl_._has_bits_[0] |= 0x00000002u;
  if (_impl_.anyjson_ == nullptr) {
    auto* p = CreateMaybeMessage<::PROTOBUF_NAMESPACE_ID::Value>(GetArenaForAllocation());
    _impl_.anyjson_ = p;
  }
  return _impl_.anyjson_;
}
inline ::PROTOBUF_NAMESPACE_ID::Value* Request::mutable_anyjson() {
  ::PROTOBUF_NAMESPACE_ID::Value* _msg = _internal_mutable_anyjson();
  // @@protoc_insertion_point(field_mutable:com.xcyber360.api.engine.test.Request.anyJSON)
  return _msg;
}
inline void Request::set_allocated_anyjson(::PROTOBUF_NAMESPACE_ID::Value* anyjson) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaForAllocation();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.anyjson_);
  }
  if (anyjson) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
        ::PROTOBUF_NAMESPACE_ID::Arena::InternalGetOwningArena(
                reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(anyjson));
    if (message_arena != submessage_arena) {
      anyjson = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, anyjson, submessage_arena);
    }
    _impl_._has_bits_[0] |= 0x00000002u;
  } else {
    _impl_._has_bits_[0] &= ~0x00000002u;
  }
  _impl_.anyjson_ = anyjson;
  // @@protoc_insertion_point(field_set_allocated:com.xcyber360.api.engine.test.Request.anyJSON)
}

// -------------------------------------------------------------------

// Response

// .com.xcyber360.api.engine.ReturnStatus status = 1;
inline void Response::clear_status() {
  _impl_.status_ = 0;
}
inline ::com::xcyber360::api::engine::ReturnStatus Response::_internal_status() const {
  return static_cast< ::com::xcyber360::api::engine::ReturnStatus >(_impl_.status_);
}
inline ::com::xcyber360::api::engine::ReturnStatus Response::status() const {
  // @@protoc_insertion_point(field_get:com.xcyber360.api.engine.test.Response.status)
  return _internal_status();
}
inline void Response::_internal_set_status(::com::xcyber360::api::engine::ReturnStatus value) {
  
  _impl_.status_ = value;
}
inline void Response::set_status(::com::xcyber360::api::engine::ReturnStatus value) {
  _internal_set_status(value);
  // @@protoc_insertion_point(field_set:com.xcyber360.api.engine.test.Response.status)
}

// optional string error = 2;
inline bool Response::_internal_has_error() const {
  bool value = (_impl_._has_bits_[0] & 0x00000001u) != 0;
  return value;
}
inline bool Response::has_error() const {
  return _internal_has_error();
}
inline void Response::clear_error() {
  _impl_.error_.ClearToEmpty();
  _impl_._has_bits_[0] &= ~0x00000001u;
}
inline const std::string& Response::error() const {
  // @@protoc_insertion_point(field_get:com.xcyber360.api.engine.test.Response.error)
  return _internal_error();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void Response::set_error(ArgT0&& arg0, ArgT... args) {
 _impl_._has_bits_[0] |= 0x00000001u;
 _impl_.error_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:com.xcyber360.api.engine.test.Response.error)
}
inline std::string* Response::mutable_error() {
  std::string* _s = _internal_mutable_error();
  // @@protoc_insertion_point(field_mutable:com.xcyber360.api.engine.test.Response.error)
  return _s;
}
inline const std::string& Response::_internal_error() const {
  return _impl_.error_.Get();
}
inline void Response::_internal_set_error(const std::string& value) {
  _impl_._has_bits_[0] |= 0x00000001u;
  _impl_.error_.Set(value, GetArenaForAllocation());
}
inline std::string* Response::_internal_mutable_error() {
  _impl_._has_bits_[0] |= 0x00000001u;
  return _impl_.error_.Mutable(GetArenaForAllocation());
}
inline std::string* Response::release_error() {
  // @@protoc_insertion_point(field_release:com.xcyber360.api.engine.test.Response.error)
  if (!_internal_has_error()) {
    return nullptr;
  }
  _impl_._has_bits_[0] &= ~0x00000001u;
  auto* p = _impl_.error_.Release();
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.error_.IsDefault()) {
    _impl_.error_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  return p;
}
inline void Response::set_allocated_error(std::string* error) {
  if (error != nullptr) {
    _impl_._has_bits_[0] |= 0x00000001u;
  } else {
    _impl_._has_bits_[0] &= ~0x00000001u;
  }
  _impl_.error_.SetAllocated(error, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.error_.IsDefault()) {
    _impl_.error_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:com.xcyber360.api.engine.test.Response.error)
}

// optional .google.protobuf.Value valueObj = 3;
inline bool Response::_internal_has_valueobj() const {
  bool value = (_impl_._has_bits_[0] & 0x00000004u) != 0;
  PROTOBUF_ASSUME(!value || _impl_.valueobj_ != nullptr);
  return value;
}
inline bool Response::has_valueobj() const {
  return _internal_has_valueobj();
}
inline const ::PROTOBUF_NAMESPACE_ID::Value& Response::_internal_valueobj() const {
  const ::PROTOBUF_NAMESPACE_ID::Value* p = _impl_.valueobj_;
  return p != nullptr ? *p : reinterpret_cast<const ::PROTOBUF_NAMESPACE_ID::Value&>(
      ::PROTOBUF_NAMESPACE_ID::_Value_default_instance_);
}
inline const ::PROTOBUF_NAMESPACE_ID::Value& Response::valueobj() const {
  // @@protoc_insertion_point(field_get:com.xcyber360.api.engine.test.Response.valueObj)
  return _internal_valueobj();
}
inline void Response::unsafe_arena_set_allocated_valueobj(
    ::PROTOBUF_NAMESPACE_ID::Value* valueobj) {
  if (GetArenaForAllocation() == nullptr) {
    delete reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.valueobj_);
  }
  _impl_.valueobj_ = valueobj;
  if (valueobj) {
    _impl_._has_bits_[0] |= 0x00000004u;
  } else {
    _impl_._has_bits_[0] &= ~0x00000004u;
  }
  // @@protoc_insertion_point(field_unsafe_arena_set_allocated:com.xcyber360.api.engine.test.Response.valueObj)
}
inline ::PROTOBUF_NAMESPACE_ID::Value* Response::release_valueobj() {
  _impl_._has_bits_[0] &= ~0x00000004u;
  ::PROTOBUF_NAMESPACE_ID::Value* temp = _impl_.valueobj_;
  _impl_.valueobj_ = nullptr;
#ifdef PROTOBUF_FORCE_COPY_IN_RELEASE
  auto* old =  reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(temp);
  temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  if (GetArenaForAllocation() == nullptr) { delete old; }
#else  // PROTOBUF_FORCE_COPY_IN_RELEASE
  if (GetArenaForAllocation() != nullptr) {
    temp = ::PROTOBUF_NAMESPACE_ID::internal::DuplicateIfNonNull(temp);
  }
#endif  // !PROTOBUF_FORCE_COPY_IN_RELEASE
  return temp;
}
inline ::PROTOBUF_NAMESPACE_ID::Value* Response::unsafe_arena_release_valueobj() {
  // @@protoc_insertion_point(field_release:com.xcyber360.api.engine.test.Response.valueObj)
  _impl_._has_bits_[0] &= ~0x00000004u;
  ::PROTOBUF_NAMESPACE_ID::Value* temp = _impl_.valueobj_;
  _impl_.valueobj_ = nullptr;
  return temp;
}
inline ::PROTOBUF_NAMESPACE_ID::Value* Response::_internal_mutable_valueobj() {
  _impl_._has_bits_[0] |= 0x00000004u;
  if (_impl_.valueobj_ == nullptr) {
    auto* p = CreateMaybeMessage<::PROTOBUF_NAMESPACE_ID::Value>(GetArenaForAllocation());
    _impl_.valueobj_ = p;
  }
  return _impl_.valueobj_;
}
inline ::PROTOBUF_NAMESPACE_ID::Value* Response::mutable_valueobj() {
  ::PROTOBUF_NAMESPACE_ID::Value* _msg = _internal_mutable_valueobj();
  // @@protoc_insertion_point(field_mutable:com.xcyber360.api.engine.test.Response.valueObj)
  return _msg;
}
inline void Response::set_allocated_valueobj(::PROTOBUF_NAMESPACE_ID::Value* valueobj) {
  ::PROTOBUF_NAMESPACE_ID::Arena* message_arena = GetArenaForAllocation();
  if (message_arena == nullptr) {
    delete reinterpret_cast< ::PROTOBUF_NAMESPACE_ID::MessageLite*>(_impl_.valueobj_);
  }
  if (valueobj) {
    ::PROTOBUF_NAMESPACE_ID::Arena* submessage_arena =
        ::PROTOBUF_NAMESPACE_ID::Arena::InternalGetOwningArena(
                reinterpret_cast<::PROTOBUF_NAMESPACE_ID::MessageLite*>(valueobj));
    if (message_arena != submessage_arena) {
      valueobj = ::PROTOBUF_NAMESPACE_ID::internal::GetOwnedMessage(
          message_arena, valueobj, submessage_arena);
    }
    _impl_._has_bits_[0] |= 0x00000004u;
  } else {
    _impl_._has_bits_[0] &= ~0x00000004u;
  }
  _impl_.valueobj_ = valueobj;
  // @@protoc_insertion_point(field_set_allocated:com.xcyber360.api.engine.test.Response.valueObj)
}

// optional string valueString = 4;
inline bool Response::_internal_has_valuestring() const {
  bool value = (_impl_._has_bits_[0] & 0x00000002u) != 0;
  return value;
}
inline bool Response::has_valuestring() const {
  return _internal_has_valuestring();
}
inline void Response::clear_valuestring() {
  _impl_.valuestring_.ClearToEmpty();
  _impl_._has_bits_[0] &= ~0x00000002u;
}
inline const std::string& Response::valuestring() const {
  // @@protoc_insertion_point(field_get:com.xcyber360.api.engine.test.Response.valueString)
  return _internal_valuestring();
}
template <typename ArgT0, typename... ArgT>
inline PROTOBUF_ALWAYS_INLINE
void Response::set_valuestring(ArgT0&& arg0, ArgT... args) {
 _impl_._has_bits_[0] |= 0x00000002u;
 _impl_.valuestring_.Set(static_cast<ArgT0 &&>(arg0), args..., GetArenaForAllocation());
  // @@protoc_insertion_point(field_set:com.xcyber360.api.engine.test.Response.valueString)
}
inline std::string* Response::mutable_valuestring() {
  std::string* _s = _internal_mutable_valuestring();
  // @@protoc_insertion_point(field_mutable:com.xcyber360.api.engine.test.Response.valueString)
  return _s;
}
inline const std::string& Response::_internal_valuestring() const {
  return _impl_.valuestring_.Get();
}
inline void Response::_internal_set_valuestring(const std::string& value) {
  _impl_._has_bits_[0] |= 0x00000002u;
  _impl_.valuestring_.Set(value, GetArenaForAllocation());
}
inline std::string* Response::_internal_mutable_valuestring() {
  _impl_._has_bits_[0] |= 0x00000002u;
  return _impl_.valuestring_.Mutable(GetArenaForAllocation());
}
inline std::string* Response::release_valuestring() {
  // @@protoc_insertion_point(field_release:com.xcyber360.api.engine.test.Response.valueString)
  if (!_internal_has_valuestring()) {
    return nullptr;
  }
  _impl_._has_bits_[0] &= ~0x00000002u;
  auto* p = _impl_.valuestring_.Release();
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.valuestring_.IsDefault()) {
    _impl_.valuestring_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  return p;
}
inline void Response::set_allocated_valuestring(std::string* valuestring) {
  if (valuestring != nullptr) {
    _impl_._has_bits_[0] |= 0x00000002u;
  } else {
    _impl_._has_bits_[0] &= ~0x00000002u;
  }
  _impl_.valuestring_.SetAllocated(valuestring, GetArenaForAllocation());
#ifdef PROTOBUF_FORCE_COPY_DEFAULT_STRING
  if (_impl_.valuestring_.IsDefault()) {
    _impl_.valuestring_.Set("", GetArenaForAllocation());
  }
#endif // PROTOBUF_FORCE_COPY_DEFAULT_STRING
  // @@protoc_insertion_point(field_set_allocated:com.xcyber360.api.engine.test.Response.valueString)
}

#ifdef __GNUC__
  #pragma GCC diagnostic pop
#endif  // __GNUC__
// -------------------------------------------------------------------


// @@protoc_insertion_point(namespace_scope)

}  // namespace test
}  // namespace engine
}  // namespace api
}  // namespace xcyber360
}  // namespace com

// @@protoc_insertion_point(global_scope)

#include <google/protobuf/port_undef.inc>
#endif  // GOOGLE_PROTOBUF_INCLUDED_GOOGLE_PROTOBUF_INCLUDED_request_5fresponse_2eproto
