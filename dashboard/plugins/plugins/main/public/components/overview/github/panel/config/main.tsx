/*
 * Xcyber360 app - GitHub Panel tab - Main layout configuration
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
import { AggTable } from '../../../../common/modules/panel';
import { EuiFlexItem } from '@elastic/eui';
import { ModuleConfigProps } from './module-config';

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
              <EuiFlexItem grow={props.width}>
                <AggTable
                  tableTitle='Actors'
                  aggTerm='data.github.actor'
                  aggLabel='Actor'
                  maxRows={5}
                  onRowClick={props.onRowClick}
                  searchParams={searchParams}
                />
              </EuiFlexItem>
            ),
          },
          {
            width: 50,
            component: props => (
              <EuiFlexItem grow={props.width}>
                <AggTable
                  tableTitle='Organizations'
                  aggTerm='data.github.org'
                  aggLabel='Organization'
                  maxRows={5}
                  onRowClick={props.onRowClick}
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
              <EuiFlexItem grow={props.width}>
                <AggTable
                  tableTitle='Repositories'
                  aggTerm='data.github.repo'
                  aggLabel='Repository'
                  maxRows={5}
                  onRowClick={props.onRowClick}
                  searchParams={searchParams}
                />
              </EuiFlexItem>
            ),
          },
          {
            width: 50,
            component: props => (
              <EuiFlexItem grow={props.width}>
                <AggTable
                  tableTitle='Actions'
                  aggTerm='data.github.action'
                  aggLabel='Action'
                  maxRows={5}
                  onRowClick={props.onRowClick}
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
