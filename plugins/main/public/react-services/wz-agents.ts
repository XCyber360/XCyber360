/*
 * Xcyber360 app - Services related to agents
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */
import { ErrorToastOptions } from 'opensearch_dashboards/public';
import { XCYBER360_AGENTS_OS_TYPE } from '../../common/constants';
import { getToasts } from '../kibana-services';
import { UnsupportedComponents } from '../utils/components-os-support';
import IApiResponse from './interfaces/api-response.interface';
import { WzRequest } from './wz-request';

export function getAgentOSType(agent) {
  if (agent?.os?.uname?.toLowerCase().includes(XCYBER360_AGENTS_OS_TYPE.LINUX)) {
    return XCYBER360_AGENTS_OS_TYPE.LINUX;
  } else if (agent?.os?.platform === XCYBER360_AGENTS_OS_TYPE.WINDOWS) {
    return XCYBER360_AGENTS_OS_TYPE.WINDOWS;
  } else if (agent?.os?.platform === XCYBER360_AGENTS_OS_TYPE.SUNOS) {
    return XCYBER360_AGENTS_OS_TYPE.SUNOS;
  } else if (agent?.os?.platform === XCYBER360_AGENTS_OS_TYPE.DARWIN) {
    return XCYBER360_AGENTS_OS_TYPE.DARWIN;
  } else {
    return XCYBER360_AGENTS_OS_TYPE.OTHERS;
  }
}

export function hasAgentSupportModule(agent, component) {
  const agentOSType = getAgentOSType(agent);
  return !UnsupportedComponents[agentOSType].includes(component);
}
