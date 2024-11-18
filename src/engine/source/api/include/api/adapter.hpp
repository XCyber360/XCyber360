#ifndef _API_ADAPTER_HPP
#define _API_ADAPTER_HPP

#include <type_traits>
#include <variant>

#include <base/utils/xcyber360Protocol/xcyber360Request.hpp>
#include <base/utils/xcyber360Protocol/xcyber360Response.hpp>
#include <eMessages/eMessage.h>
#include <eMessages/engine.pb.h>

namespace api::adapter
{

/**
 * @brief Return a Xcyber360Response with de eMessage serialized or a Xcyber360Response with the error if it fails
 * @tparam T
 * @param eMessage
 * @return base::utils::xcyber360Protocol::Xcyber360Response
 */
template<typename T>
base::utils::xcyber360Protocol::Xcyber360Response toXcyber360Response(const T& eMessage)
{
    // Check that T is derived from google::protobuf::Message
    static_assert(std::is_base_of<google::protobuf::Message, T>::value, "T must be a derived class of proto::Message");

    const auto res = eMessage::eMessageToJson<T>(eMessage);

    if (std::holds_alternative<base::Error>(res))
    {
        const auto& error = std::get<base::Error>(res);
        return base::utils::xcyber360Protocol::Xcyber360Response::internalError(error.message);
    }
    return base::utils::xcyber360Protocol::Xcyber360Response {json::Json {std::get<std::string>(res).c_str()}};
}

/**
 * @brief Return a variant with the parsed eMessage or a Xcyber360Response with the error
 *
 * @tparam T Request type
 * @tparam U Response type
 * @param json
 * @return std::variant<base::utils::xcyber360Protocol::Xcyber360Response, T>
 */
template<typename T, typename U>
std::variant<base::utils::xcyber360Protocol::Xcyber360Response, T>
fromXcyber360Request(const base::utils::xcyber360Protocol::Xcyber360Request& wRequest)
{
    // Check that T and U are derived from google::protobuf::Message
    static_assert(std::is_base_of<google::protobuf::Message, T>::value, "T must be a derived class of proto::Message");
    static_assert(std::is_base_of<google::protobuf::Message, U>::value, "U must be a derived class of proto::Message");
    // Check that U has set_status and set_error functions
    static_assert(std::is_invocable_v<decltype(&U::set_status), U, ::com::xcyber360::api::engine::ReturnStatus>,
                  "U must have set_status function");
    // static_assert(std::is_invocable_v<decltype(&U::set_error), U, const std::string&>,
    //               "U must have set_error function");

    const auto json = wRequest.getParameters().value_or(json::Json {"{}"}).str();

    auto res = eMessage::eMessageFromJson<T>(json);
    if (std::holds_alternative<base::Error>(res))
    {
        U eResponse;
        eResponse.set_status(::com::xcyber360::api::engine::ReturnStatus::ERROR);
        eResponse.set_error(std::get<base::Error>(res).message);
        return toXcyber360Response<U>(eResponse);
    }

    return std::move(std::get<T>(res));
}

/**
 * @brief Return a Xcyber360Response with the genericError in Xcyber360Response
 *
 * @tparam T Response type
 * @param std::string Error message
 * @return std::variant<base::utils::xcyber360Protocol::Xcyber360Response, T>
 */
template<typename T>
base::utils::xcyber360Protocol::Xcyber360Response genericError(const std::string& message)
{
    // Check that T is derived from google::protobuf::Message
    static_assert(std::is_base_of<google::protobuf::Message, T>::value, "T must be a derived class of proto::Message");
    static_assert(std::is_invocable_v<decltype(&T::set_status), T, ::com::xcyber360::api::engine::ReturnStatus>,
                  "T must have set_status function");

    T eResponse;
    eResponse.set_status(::com::xcyber360::api::engine::ReturnStatus::ERROR);
    eResponse.set_error(message.data());
    return toXcyber360Response<T>(eResponse);
}

/**
 * @brief Return a Xcyber360Response with the status OK in Xcyber360Response
 *
 * @tparam T Response type
 * @return std::variant<base::utils::xcyber360Protocol::Xcyber360Response, T>
 */
template<typename T>
base::utils::xcyber360Protocol::Xcyber360Response genericSuccess()
{
    // Check that T is derived from google::protobuf::Message
    static_assert(std::is_base_of<google::protobuf::Message, T>::value, "T must be a derived class of proto::Message");
    static_assert(std::is_invocable_v<decltype(&T::set_status), T, ::com::xcyber360::api::engine::ReturnStatus>,
                  "T must have set_status function");

    T eResponse;
    eResponse.set_status(::com::xcyber360::api::engine::ReturnStatus::OK);
    return toXcyber360Response<T>(eResponse);
}

} // namespace api::adapter

#endif // _API_ADAPTER_HPP
