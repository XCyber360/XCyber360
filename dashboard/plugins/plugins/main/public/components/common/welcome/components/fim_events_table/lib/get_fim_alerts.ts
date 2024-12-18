/*
 * Xcyber360 app - React component building the welcome screen of an agent.
 * version, OS, registration date, last keep alive.
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
import {
  getIndexPattern,
  getElasticAlerts,
  IFilterParams,
} from '../../../../../../react-services';
import { buildPhraseFilter } from '../../../../../../../../../src/plugins/data/common';

import { AppState } from '../../../../../../react-services/app-state';

function createFilters(agentId, indexPattern) {
  const filter = filter => {
    return {
      ...buildPhraseFilter(
        { name: filter.name, type: 'text' },
        filter.value,
        indexPattern,
      ),
      $state: { store: 'appState' },
    };
  };
  const xcyber360Filter = getXcyber360Filter();
  const filters = [
    xcyber360Filter,
    { name: 'agent.id', value: agentId },
    { name: 'rule.groups', value: 'syscheck' },
  ];
  return filters.map(filter);
}

export function getXcyber360Filter() {
  const clusterInfo = AppState.getClusterInfo();
  const xcyber360Filter = {
    name: clusterInfo.status === 'enabled' ? 'cluster.name' : 'manager.name',
    value:
      clusterInfo.status === 'enabled'
        ? clusterInfo.cluster
        : clusterInfo.manager,
  };
  return xcyber360Filter;
}

export async function getFimAlerts(agentId, time, sortObj) {
  const indexPattern = await getIndexPattern();
  const sort = [{ [sortObj.field.substring(8)]: sortObj.direction }];
  const filterParams: IFilterParams = {
    filters: createFilters(agentId, indexPattern),
    query: { query: '', language: 'kuery' },
    time,
  };
  const response = await getElasticAlerts(
    indexPattern,
    filterParams,
    {},
    { size: 5, sort },
  );
  return (((response || {}).data || {}).hits || {}).hits;
}
