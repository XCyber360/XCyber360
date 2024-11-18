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

#include "xcyber360DBQueryBuilder_test.hpp"
#include "xcyber360DBQueryBuilder.hpp"
#include <string>

TEST_F(Xcyber360DBQueryBuilderTest, GlobalTest)
{
    std::string message = Xcyber360DBQueryBuilder::builder().global().selectAll().fromTable("agent").build();
    EXPECT_EQ(message, "global sql SELECT * FROM agent ");
}

TEST_F(Xcyber360DBQueryBuilderTest, AgentTest)
{
    std::string message = Xcyber360DBQueryBuilder::builder().agent("0").selectAll().fromTable("sys_programs").build();
    EXPECT_EQ(message, "agent 0 sql SELECT * FROM sys_programs ");
}

TEST_F(Xcyber360DBQueryBuilderTest, WhereTest)
{
    std::string message = Xcyber360DBQueryBuilder::builder()
                              .agent("0")
                              .selectAll()
                              .fromTable("sys_programs")
                              .whereColumn("name")
                              .equalsTo("bash")
                              .build();
    EXPECT_EQ(message, "agent 0 sql SELECT * FROM sys_programs WHERE name = 'bash' ");
}

TEST_F(Xcyber360DBQueryBuilderTest, WhereAndTest)
{
    std::string message = Xcyber360DBQueryBuilder::builder()
                              .agent("0")
                              .selectAll()
                              .fromTable("sys_programs")
                              .whereColumn("name")
                              .equalsTo("bash")
                              .andColumn("version")
                              .equalsTo("1")
                              .build();
    EXPECT_EQ(message, "agent 0 sql SELECT * FROM sys_programs WHERE name = 'bash' AND version = '1' ");
}

TEST_F(Xcyber360DBQueryBuilderTest, WhereOrTest)
{
    std::string message = Xcyber360DBQueryBuilder::builder()
                              .agent("0")
                              .selectAll()
                              .fromTable("sys_programs")
                              .whereColumn("name")
                              .equalsTo("bash")
                              .orColumn("version")
                              .equalsTo("1")
                              .build();
    EXPECT_EQ(message, "agent 0 sql SELECT * FROM sys_programs WHERE name = 'bash' OR version = '1' ");
}

TEST_F(Xcyber360DBQueryBuilderTest, WhereIsNullTest)
{
    std::string message = Xcyber360DBQueryBuilder::builder()
                              .agent("0")
                              .selectAll()
                              .fromTable("sys_programs")
                              .whereColumn("name")
                              .isNull()
                              .build();
    EXPECT_EQ(message, "agent 0 sql SELECT * FROM sys_programs WHERE name IS NULL ");
}

TEST_F(Xcyber360DBQueryBuilderTest, WhereIsNotNullTest)
{
    std::string message = Xcyber360DBQueryBuilder::builder()
                              .agent("0")
                              .selectAll()
                              .fromTable("sys_programs")
                              .whereColumn("name")
                              .isNotNull()
                              .build();
    EXPECT_EQ(message, "agent 0 sql SELECT * FROM sys_programs WHERE name IS NOT NULL ");
}

TEST_F(Xcyber360DBQueryBuilderTest, InvalidValue)
{
    EXPECT_THROW(Xcyber360DBQueryBuilder::builder()
                     .agent("0")
                     .selectAll()
                     .fromTable("sys_programs")
                     .whereColumn("name")
                     .equalsTo("bash'")
                     .build(),
                 std::runtime_error);
}

TEST_F(Xcyber360DBQueryBuilderTest, InvalidColumn)
{
    EXPECT_THROW(Xcyber360DBQueryBuilder::builder()
                     .agent("0")
                     .selectAll()
                     .fromTable("sys_programs")
                     .whereColumn("name'")
                     .equalsTo("bash")
                     .build(),
                 std::runtime_error);
}

TEST_F(Xcyber360DBQueryBuilderTest, InvalidTable)
{
    EXPECT_THROW(Xcyber360DBQueryBuilder::builder()
                     .agent("0")
                     .selectAll()
                     .fromTable("sys_programs'")
                     .whereColumn("name")
                     .equalsTo("bash")
                     .build(),
                 std::runtime_error);
}

TEST_F(Xcyber360DBQueryBuilderTest, GlobalGetCommand)
{
    std::string message = Xcyber360DBQueryBuilder::builder().globalGetCommand("agent-info 1").build();
    EXPECT_EQ(message, "global get-agent-info 1 ");
}

TEST_F(Xcyber360DBQueryBuilderTest, GlobalFindCommand)
{
    std::string message = Xcyber360DBQueryBuilder::builder().globalFindCommand("agent 1").build();
    EXPECT_EQ(message, "global find-agent 1 ");
}

TEST_F(Xcyber360DBQueryBuilderTest, GlobalSelectCommand)
{
    std::string message = Xcyber360DBQueryBuilder::builder().globalSelectCommand("agent-name 1").build();
    EXPECT_EQ(message, "global select-agent-name 1 ");
}

TEST_F(Xcyber360DBQueryBuilderTest, AgentGetOsInfoCommand)
{
    std::string message = Xcyber360DBQueryBuilder::builder().agentGetOsInfoCommand("1").build();
    EXPECT_EQ(message, "agent 1 osinfo get ");
}

TEST_F(Xcyber360DBQueryBuilderTest, AgentGetHotfixesCommand)
{
    std::string message = Xcyber360DBQueryBuilder::builder().agentGetHotfixesCommand("1").build();
    EXPECT_EQ(message, "agent 1 hotfix get ");
}

TEST_F(Xcyber360DBQueryBuilderTest, AgentGetPackagesCommand)
{
    std::string message = Xcyber360DBQueryBuilder::builder().agentGetPackagesCommand("1").build();
    EXPECT_EQ(message, "agent 1 package get ");
}
