/*
 * Xcyber360 app - React component for building the WzMenu component.
 *
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 *
 */
import WzAgentSelector from './wz-agent-selector';
import { compose } from 'redux';
import { withErrorBoundary } from '../common/hocs';

export const WzAgentSelectorWrapper =
  compose(withErrorBoundary)(WzAgentSelector);
