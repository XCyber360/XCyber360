/*
 * Xcyber360 - Shared Modules utils
 * Copyright (C) 2015, Xcyber360 Inc.
 * April 25, 2023.
 *
 * This program is free software; you can redistribute it
 * and/or modify it under the terms of the GNU General Public
 * License (version 2) as published by the FSF - Free Software
 * Foundation.
 */

#ifndef _I_DATA_PROVIDER_HPP
#define _I_DATA_PROVIDER_HPP
#include <cstddef>
#include <cstdint>

namespace Xz
{
    /**
     * @brief Data provider interface for the XZ wrapper
     *
     */
    class IDataProvider
    {
    public:
        /**
         * @brief Struct that represents a block of data to be processed by the Xz wrapper
         *
         */
        struct DataBlock
        {
            // cppcheck-suppress unusedStructMember
            const uint8_t* data {}; ///< Pointer to the start of the data block
            // cppcheck-suppress unusedStructMember
            size_t dataLen {}; ///< Size of the data block
        };

        // LCOV_EXCL_START
        virtual ~IDataProvider() = default;
        // LCOV_EXCL_STOP

        /**
         * @brief Called at the start of the process so that the provider can initialize its internal state
         *
         */
        virtual void begin() = 0;

        /**
         * @brief Get the next input data block
         * @details When the returned dataLen is 0 it signals that there is no more data to be processed.
         * @return DataBlock
         */
        virtual DataBlock getNextBlock() = 0;
    };
} // namespace Xz
#endif // _I_DATA_PROVIDER_HPP
