/*
 * Xcyber360 app - GitHub Panel tab - Drilldown layout configuration
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

import React, { useState, useMemo, useEffect } from 'react';
import {
  EuiFlexItem,
  EuiPanel,
  EuiToolTip,
  EuiButtonIcon,
  EuiDataGridCellValueElementProps,
  EuiDataGrid,
  EuiLink,
} from '@elastic/eui';
import { SecurityAlerts } from '../../../../visualize/components';
import { ViewMode } from '../../../../../../../../src/plugins/embeddable/public';
import { getPlugins, getCore } from '../../../../../kibana-services';
import { DashboardPanelState } from '../../../../../../../../src/plugins/dashboard/public/application';
import { EmbeddableInput } from '../../../../../../../../src/plugins/embeddable/public';
import {
  getVisStateTopActors,
  getVisStateRuleLevelEvolution,
  getVisStateTopCountries,
  getVisStateTopRepositories,
  getVisStateTopActions,
} from './visualizations';
import { ModuleConfigProps } from './module-config';
import {
  ErrorFactory,
  HttpError,
  ErrorHandler,
} from '../../../../../react-services/error-management';
import DrillDownDataGrid from './drilldown-data-grid';
import { rules } from '../../../../../utils/applications';
import { RedirectAppLinks } from '../../../../../../../../src/plugins/opensearch_dashboards_react/public';

const DashboardByRenderer =
  getPlugins().dashboard.DashboardContainerByValueRenderer;

const getDashboardPanels = (
  indexPatternId: string,
): {
  [panelId: string]: DashboardPanelState<
    EmbeddableInput & { [k: string]: unknown }
  >;
} => {
  return {
    d0: {
      gridData: {
        w: 16,
        h: 11,
        x: 0,
        y: 0,
        i: 'd0',
      },
      type: 'visualization',
      explicitInput: {
        id: 'd0',
        savedVis: getVisStateTopActions(indexPatternId),
      },
    },
    d1: {
      gridData: {
        w: 16,
        h: 11,
        x: 16,
        y: 0,
        i: 'd1',
      },
      type: 'visualization',
      explicitInput: {
        id: 'd1',
        savedVis: getVisStateTopRepositories(indexPatternId),
      },
    },
    d2: {
      gridData: {
        w: 16,
        h: 11,
        x: 32,
        y: 0,
        i: 'd2',
      },
      type: 'visualization',
      explicitInput: {
        id: 'd2',
        savedVis: getVisStateTopActors(indexPatternId),
      },
    },
    d3: {
      gridData: {
        w: 24,
        h: 11,
        x: 0,
        y: 11,
        i: 'd3',
      },
      type: 'visualization',
      explicitInput: {
        id: 'd3',
        savedVis: getVisStateTopCountries(indexPatternId),
      },
    },
    d4: {
      gridData: {
        w: 24,
        h: 11,
        x: 24,
        y: 11,
        i: 'd4',
      },
      type: 'visualization',
      explicitInput: {
        id: 'd4',
        savedVis: getVisStateRuleLevelEvolution(indexPatternId),
      },
    },
  };
};

export const DrilldownConfigOrganization = (
  drilldownProps: ModuleConfigProps,
) => {
  const { fetchData, fetchFilters, searchBarProps, indexPattern } =
    drilldownProps;

  return {
    rows: [
      {
        columns: [
          {
            width: 100,
            component: props => {
              return (
                <div style={{ width: '100%' }}>
                  <DashboardByRenderer
                    input={{
                      viewMode: ViewMode.VIEW,
                      panels: getDashboardPanels(indexPattern.id),
                      isFullScreenMode: false,
                      filters: fetchFilters ?? [],
                      useMargins: true,
                      id: 'github-drilldown-action-dashboard-tab',
                      timeRange: searchBarProps?.absoluteDateRange,
                      title: 'GitHub drilldown action dashboard',
                      description: 'Dashboard of the GitHub drilldown action',
                      query: searchBarProps.query,
                      refreshConfig: {
                        pause: false,
                        value: 15,
                      },
                      hidePanelTitles: false,
                    }}
                    onInputUpdated={() => {}}
                  />
                </div>
              );
            },
          },
        ],
      },
      {
        columns: [
          {
            width: 100,
            component: () => {
              const defaultTableColumns = [
                {
                  id: 'timestamp',
                  isSortable: true,
                  defaultSortDirection: 'desc',
                },
                { id: 'rule.description' },
                { id: 'data.github.repo', displayAsText: 'Repository' },
                { id: 'data.github.actor', displayAsText: 'Actor' },
                { id: 'data.github.action', displayAsText: 'Action' },
                { id: 'rule.level' },
                { id: 'rule.id' },
              ];

              return (
                <DrillDownDataGrid
                  defaultTableColumns={defaultTableColumns}
                  fetchData={fetchData}
                  fetchFilters={fetchFilters}
                  searchBarProps={searchBarProps}
                  indexPattern={indexPattern}
                />
              );
            },
          },
        ],
      },
    ],
  };
};
