#ifndef _WDB_IWDB_MANAGER_HPP
#define _WDB_IWDB_MANAGER_HPP

#include <memory>

#include <wdb/iwdbHandler.hpp>

namespace xcyber360db
{

class IWDBManager
{
public:
    virtual ~IWDBManager() = default;

    virtual std::shared_ptr<IWDBHandler> connection() = 0;
};

} // namespace xcyber360db

#endif // _WDB_IWDB_MANAGER_HPP
