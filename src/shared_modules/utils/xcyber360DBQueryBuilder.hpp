/*
 * Xcyber360 DB Query Builder
 * Copyright (C) 2015, Xcyber360 Inc.
 * October 31, 2023.
 *
 * This program is free software; you can redistribute it
 * and/or modify it under the terms of the GNU General Public
 * License (version 2) as published by the FSF - Free Software
 * Foundation.
 */

#ifndef _XCYBER360_DB_QUERY_BUILDER_HPP
#define _XCYBER360_DB_QUERY_BUILDER_HPP

#include "builder.hpp"
#include "stringHelper.h"
#include <string>

constexpr auto XCYBER360_DB_ALLOWED_CHARS {"-_ "};

class Xcyber360DBQueryBuilder final : public Utils::Builder<Xcyber360DBQueryBuilder>
{
private:
    std::string m_query;

public:
    Xcyber360DBQueryBuilder& global()
    {
        m_query += "global sql ";
        return *this;
    }

    Xcyber360DBQueryBuilder& agent(const std::string& id)
    {
        if (!Utils::isNumber(id))
        {
            throw std::runtime_error("Invalid agent id");
        }

        m_query += "agent " + id + " sql ";
        return *this;
    }

    Xcyber360DBQueryBuilder& selectAll()
    {
        m_query += "SELECT * ";
        return *this;
    }

    Xcyber360DBQueryBuilder& fromTable(const std::string& table)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(table, XCYBER360_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid table name");
        }
        m_query += "FROM " + table + " ";
        return *this;
    }

    Xcyber360DBQueryBuilder& whereColumn(const std::string& column)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(column, XCYBER360_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid column name");
        }
        m_query += "WHERE " + column + " ";
        return *this;
    }

    Xcyber360DBQueryBuilder& isNull()
    {
        m_query += "IS NULL ";
        return *this;
    }

    Xcyber360DBQueryBuilder& isNotNull()
    {
        m_query += "IS NOT NULL ";
        return *this;
    }

    Xcyber360DBQueryBuilder& equalsTo(const std::string& value)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(value, XCYBER360_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid value");
        }
        m_query += "= '" + value + "' ";
        return *this;
    }

    Xcyber360DBQueryBuilder& andColumn(const std::string& column)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(column, XCYBER360_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid column name");
        }
        m_query += "AND " + column + " ";
        return *this;
    }

    Xcyber360DBQueryBuilder& orColumn(const std::string& column)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(column, XCYBER360_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid column name");
        }
        m_query += "OR " + column + " ";
        return *this;
    }

    Xcyber360DBQueryBuilder& globalGetCommand(const std::string& command)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(command, XCYBER360_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid command");
        }
        m_query += "global get-" + command + " ";
        return *this;
    }

    Xcyber360DBQueryBuilder& globalFindCommand(const std::string& command)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(command, XCYBER360_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid command");
        }
        m_query += "global find-" + command + " ";
        return *this;
    }

    Xcyber360DBQueryBuilder& globalSelectCommand(const std::string& command)
    {
        if (!Utils::isAlphaNumericWithSpecialCharacters(command, XCYBER360_DB_ALLOWED_CHARS))
        {
            throw std::runtime_error("Invalid command");
        }
        m_query += "global select-" + command + " ";
        return *this;
    }

    Xcyber360DBQueryBuilder& agentGetOsInfoCommand(const std::string& id)
    {
        if (!Utils::isNumber(id))
        {
            throw std::runtime_error("Invalid agent id");
        }
        m_query += "agent " + id + " osinfo get ";
        return *this;
    }

    Xcyber360DBQueryBuilder& agentGetHotfixesCommand(const std::string& id)
    {
        if (!Utils::isNumber(id))
        {
            throw std::runtime_error("Invalid agent id");
        }
        m_query += "agent " + id + " hotfix get ";
        return *this;
    }

    Xcyber360DBQueryBuilder& agentGetPackagesCommand(const std::string& id)
    {
        if (!Utils::isNumber(id))
        {
            throw std::runtime_error("Invalid agent id");
        }
        m_query += "agent " + id + " package get ";
        return *this;
    }

    std::string build()
    {
        return m_query;
    }
};

#endif /* _XCYBER360_DB_QUERY_BUILDER_HPP */
