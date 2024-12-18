/*
 * Xcyber360 app - Office 365 MainViewConfig.
 *
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

import React from 'react';
import { AggTable } from '../../../../common/modules/panel/';
import { EuiFlexItem } from '@elastic/eui';
import { SecurityAlerts } from '../../../../visualize/components';

export const MainViewConfig = (props: ModuleConfigProps) => {

  const { fetchFilters, searchBarProps, indexPattern } = props;

  const searchParams = {
    filters: fetchFilters,
    indexPattern,
    query: searchBarProps.query,
    dateRange: {
      from: searchBarProps.dateRangeFrom || '',
      to: searchBarProps.dateRangeTo || '',
    }
  };

  return {
    rows: [
      {
        columns: [
          {
            width: 50,
            component: props => (
              <EuiFlexItem grow={props.grow}>
                <AggTable
                  tableTitle='Top users'
                  aggTerm='data.office365.UserId'
                  aggLabel='User'
                  maxRows={5}
                  onRowClick={(field, value) => props.onRowClick(field, value)}
                  searchParams={searchParams}
                />
              </EuiFlexItem>
            ),
          },
          {
            width: 50,
            component: props => (
              <EuiFlexItem grow={props.grow}>
                <AggTable
                  tableTitle='Top client IP address'
                  aggTerm='data.office365.ClientIP'
                  aggLabel='Client IP address'
                  maxRows={5}
                  onRowClick={(field, value) => props.onRowClick(field, value)}
                  searchParams={searchParams}
                />
              </EuiFlexItem>
            ),
          },
        ],
      },
      {
        columns: [
          {
            width: 50,
            component: props => (
              <EuiFlexItem grow={props.grow}>
                <AggTable
                  tableTitle='Top rules'
                  aggTerm='rule.description'
                  aggLabel='Rule'
                  maxRows={5}
                  onRowClick={(field, value) => props.onRowClick(field, value)}
                  searchParams={searchParams}
                />
              </EuiFlexItem>
            ),
          },
          {
            width: 50,
            component: props => (
              <EuiFlexItem grow={props.grow}>
                <AggTable
                  tableTitle='Top operations'
                  aggTerm='data.office365.Operation'
                  aggLabel='Operation'
                  maxRows={5}
                  onRowClick={(field, value) => props.onRowClick(field, value)}
                  searchParams={searchParams}
                />
              </EuiFlexItem>
            ),
          },
        ],
      },
    ],
  };
}
