#include <gtest/gtest.h>

#include <api/adapter.hpp>
#include <eMessages/request_response.pb.h>

using namespace api::adapter;
namespace eEngine = ::com::xcyber360::api::engine;
using RequestType = eEngine::test::Request;
using ResponseType = eEngine::test::Response;
using Xcyber360Request = base::utils::xcyber360Protocol::Xcyber360Request;
using Xcyber360Response = base::utils::xcyber360Protocol::Xcyber360Response;

TEST(Adapter_toXcyber360Response, succees_ok)
{
    ResponseType response;
    response.set_status(eEngine::ReturnStatus::OK);
    response.set_valuestring("test value");
    const auto expectedData = json::Json {R"({"valueString":"test value", "status":"OK"})"};

    const auto wResponse = toXcyber360Response(response);

    ASSERT_FALSE(wResponse.error());
    ASSERT_EQ(wResponse.data(), expectedData);
}

TEST(Adapter_toXcyber360Response, succees_inside_error)
{
    ResponseType response;
    response.set_status(eEngine::ReturnStatus::ERROR);
    response.set_error("test error");
    const auto expectedData = json::Json {R"({"status":"ERROR","error":"test error"})"};

    const auto wResponse = toXcyber360Response(response);
    ASSERT_FALSE(wResponse.error()); // The error is inside the data not in the protocol
    ASSERT_EQ(wResponse.data(), expectedData);
}

// Its difficult to test this function because it depends on the eMessage implementation
// TEST(Adapter_toXcyber360Response, noSerialized)
// {
// }

TEST(Adapter_fromXcyber360Request, success_empty)
{
    const auto json = json::Json {R"({})"};
    const auto wRequest = Xcyber360Request {json};

    const auto res = fromXcyber360Request<RequestType, ResponseType>(wRequest);

    ASSERT_TRUE(std::holds_alternative<RequestType>(res));
    const auto eRequest = std::get<RequestType>(res);
    ASSERT_EQ(eRequest.valuestring(), "");
    ASSERT_EQ(eRequest.defaultbool(), false);
    ASSERT_EQ(eRequest.defaultint(), 0);
    ASSERT_EQ(eRequest.has_anyjson(), false);
    ASSERT_EQ(eRequest.has_valuestring(), false);
}

TEST(Adapter_fromXcyber360Request, success)
{
    const auto params =
        json::Json {R"({"valueString":"test value", "defaultBool":true, "defaultInt":1, "anyJson":{}})"};
    const auto wRequest = Xcyber360Request::create("testCmd", "test origin", params);

    const auto res = fromXcyber360Request<RequestType, ResponseType>(wRequest);

    ASSERT_TRUE(std::holds_alternative<RequestType>(res));
    const auto& eRequest = std::get<RequestType>(res);
    ASSERT_EQ(eRequest.valuestring(), "test value");
    ASSERT_EQ(eRequest.defaultbool(), true);
    ASSERT_EQ(eRequest.defaultint(), 1);
    ASSERT_EQ(eRequest.has_anyjson(), false);
    ASSERT_EQ(eRequest.has_valuestring(), true);
    ASSERT_EQ(eRequest.valuestring(), "test value");
}

TEST(Adapter_fromXcyber360Request, fail_eMessageFormat)
{
    const auto params = json::Json {R"({"valueString":null, "defaultBool":"true", "defaultInt":{}})"};
    const auto wRequest = Xcyber360Request::create("testCmd", "test origin", params);

    const auto res = fromXcyber360Request<RequestType, ResponseType>(wRequest);

    // Fail because the json is not valid for the eMessage, return a wResponse with the error
    ASSERT_TRUE(std::holds_alternative<Xcyber360Response>(res));
    const auto& wResponse = std::get<Xcyber360Response>(res);
    ASSERT_FALSE(wResponse.error());

    ASSERT_EQ(wResponse.data(), json::Json(R"({"status":"ERROR",
                              "error":"INVALID_ARGUMENT:: invalid value Starting an object on a scalar field for type defaultInt"
                            })"));
}

TEST(Adapter_genericError, response_error)
{
    const auto message = std::string {"test generic error"};

    const auto wResponse = genericError<ResponseType>(message);

    ASSERT_FALSE(wResponse.error());
    ASSERT_EQ(wResponse.data(), json::Json(R"({"status":"ERROR",
                              "error":"test generic error"
                            })"));
}

TEST(Adapter_genericSuccess, response_ok)
{
    const auto message = std::string {"test generic success"};

    const auto wResponse = genericSuccess<ResponseType>();

    ASSERT_FALSE(wResponse.error());
    ASSERT_EQ(wResponse.data(), json::Json(R"({"status":"OK"})"));
}
