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

#ifndef _VECTOR_DATA_PROVIDER_HPP
#define _VECTOR_DATA_PROVIDER_HPP

#include "iDataProvider.hpp"
#include <cstddef>
#include <cstdint>
#include <vector>

namespace Xz
{
    /**
     * @brief Provides data from a byte vector
     *
     */
    class VectorDataProvider : public IDataProvider
    {
        const std::vector<uint8_t>& m_inputData; ///< Reference to the input vector
        bool hasPendingData {true};              ///< Indicates whether there is unprocessed data.

    public:
        /**
         * @brief Construct a new Vector Data Provider object
         *
         * @param inputData Vector with the input data
         */
        explicit VectorDataProvider(const std::vector<uint8_t>& inputData)
            : m_inputData(inputData)
        {
        }

        /*! @copydoc IDataProvider::begin() */
        void begin() override
        {
            hasPendingData = true;
        }

        /*! @copydoc IDataProvider::getNextBlock() */
        DataBlock getNextBlock() override
        {
            DataBlock dataBlock;
            if (hasPendingData)
            {
                // Since all the input data is already available in the input vector just provide all the data in one
                // block.
                dataBlock.data = m_inputData.data();
                dataBlock.dataLen = m_inputData.size();
                hasPendingData = false;
            }
            return dataBlock;
        }
    };
} // namespace Xz
#endif // _VECTOR_DATA_PROVIDER_HPP
