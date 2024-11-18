/*
 * Xcyber360 shared modules utils
 * Copyright (C) 2015, Xcyber360 Inc.
 * Nov 1, 2023.
 *
 * This program is free software; you can redistribute it
 * and/or modify it under the terms of the GNU General Public
 * License (version 2) as published by the FSF - Free Software
 * Foundation.
 */

#ifndef _XCYBER360_DB_QUERY_BUILDER_TEST_HPP
#define _XCYBER360_DB_QUERY_BUILDER_TEST_HPP

#include "gtest/gtest.h"

class Xcyber360DBQueryBuilderTest : public ::testing::Test
{
protected:
    Xcyber360DBQueryBuilderTest() = default;
    virtual ~Xcyber360DBQueryBuilderTest() = default;

    void SetUp() override {};
    void TearDown() override {};
};

#endif // _XCYBER360_DB_QUERY_BUILDER_TEST_HPP
