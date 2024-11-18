#ifndef _WDB_MOCK_WDB_MANAGER_HPP
#define _WDB_MOCK_WDB_MANAGER_HPP

#include <gmock/gmock.h>

#include <wdb/iwdbManager.hpp>

class MockWdbManager : public xcyber360db::IWDBManager
{
public:
    MOCK_METHOD(std::shared_ptr<xcyber360db::IWDBHandler>, connection, (), (override));
};

#endif // _WDB_MOCK_WDB_MANAGER_HPP
