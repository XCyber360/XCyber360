#include <gtest/gtest.h>

#include <base/utils/xcyber360Protocol/xcyber360Response.hpp>

TEST(Xcyber360Response, constructor)
{
    const json::Json jdata {R"({"test": "data"})"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_EQ(wresponse.data(), jdata);
    EXPECT_EQ(wresponse.error(), error);
    EXPECT_EQ(wresponse.message(), message);
}

TEST(Xcyber360Response, toString)
{
    const json::Json jdata {R"({"test": "data"})"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_EQ(wresponse.toString(), R"({"data":{"test":"data"},"error":0,"message":"test message"})");
}

TEST(Xcyber360Response, toStringNoMessage)
{
    const json::Json jdata {R"({"test": "data"})"};
    const int error {0};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error};
    EXPECT_EQ(wresponse.toString(), R"({"data":{"test":"data"},"error":0})");
}

TEST(Xcyber360Response, toStringEmptyMessage)
{
    const json::Json jdata {R"({"test": "data"})"};
    const int error {0};
    const std::string message {""};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_EQ(wresponse.toString(), R"({"data":{"test":"data"},"error":0})");
}

TEST(Xcyber360Response, toStringEmptyData)
{
    const json::Json jdata {R"({})"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_EQ(wresponse.toString(), R"({"data":{},"error":0,"message":"test message"})");
}

TEST(Xcyber360Response, toStringArrayData)
{
    const json::Json jdata {R"([{"test": "data"}])"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_EQ(wresponse.toString(), R"({"data":[{"test":"data"}],"error":0,"message":"test message"})");
}

TEST(Xcyber360Response, toStringEmptyDataEmptyMessage)
{
    const json::Json jdata {R"({})"};
    const int error {0};
    const std::string message {""};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_EQ(wresponse.toString(), R"({"data":{},"error":0})");
}

TEST(Xcyber360Response, validateOkObject)
{
    const json::Json jdata {R"({"test": "data"})"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_TRUE(wresponse.isValid());
}

TEST(Xcyber360Response, validateOkArray)
{
    const json::Json jdata {R"([{"test": "data"}])"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_TRUE(wresponse.isValid());
}

TEST(Xcyber360Response, validateOkEmptyObject)
{
    const json::Json jdata {R"({})"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_TRUE(wresponse.isValid());
}

TEST(Xcyber360Response, validateOkEmptyArray)
{
    const json::Json jdata {R"([])"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_TRUE(wresponse.isValid());
}

TEST(Xcyber360Response, validateOkEmptyMessage)
{
    const json::Json jdata {R"({"test": "data"})"};
    const int error {0};
    const std::string message {""};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_TRUE(wresponse.isValid());
}

TEST(Xcyber360Response, validateOkEmptyData)
{
    const json::Json jdata {R"({})"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_TRUE(wresponse.isValid());
}

TEST(Xcyber360Response, validateOkEmptyDataEmptyMessage)
{
    const json::Json jdata {R"({})"};
    const int error {0};
    const std::string message {""};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_TRUE(wresponse.isValid());
}

TEST(Xcyber360Response, validateErrorInvalidDataStr)
{
    const json::Json jdata {R"("test")"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_FALSE(wresponse.isValid());
}

TEST(Xcyber360Response, validateErrorInvalidDataInt)
{
    const json::Json jdata {R"(1)"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_FALSE(wresponse.isValid());
}

TEST(Xcyber360Response, validateErrorInvalidDataBool)
{
    const json::Json jdata {R"(true)"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_FALSE(wresponse.isValid());
}

TEST(Xcyber360Response, validateErrorInvalidDataNull)
{
    const json::Json jdata {R"(null)"};
    const int error {0};
    const std::string message {"test message"};
    const base::utils::xcyber360Protocol::Xcyber360Response wresponse {jdata, error, message};
    EXPECT_FALSE(wresponse.isValid());
}
