/*
 * Xcyber360 app - React component for show configuration of OpenSCAP - evaluations tab.
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

import React, { Component, Fragment } from 'react';

import { EuiBasicTable } from '@elastic/eui';

import WzConfigurationSettingsHeader from '../util-components/configuration-settings-header';
import WzNoConfig from '../util-components/no-config';
import { isString } from '../utils/utils';
import helpLinks from './help-links';

const renderProfile = item => (
  <Fragment>
    {item && item.length ? (
      <ul>
        {item.map((profile, key) => (
          <li key={`profile-${key}`}>{profile}</li>
        ))}
      </ul>
    ) : (
      '-'
    )}
  </Fragment>
);

const columns = [
  { field: 'path', name: 'Path' },
  { field: 'profile', name: 'Profile', render: renderProfile },
  { field: 'type', name: 'Type' },
  { field: 'timeout', name: 'Timeout' }
];

class WzConfigurationOpenScapEvaluations extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    const { currentConfig, wodleConfig } = this.props;
    return (
      <Fragment>
        {currentConfig['wmodules-wmodules'] &&
          isString(currentConfig['wmodules-wmodules']) && (
            <WzNoConfig
              error={currentConfig['wmodules-wmodules']}
              help={helpLinks}
            />
          )}
        {currentConfig &&
          ((wodleConfig['open-scap'] &&
          !wodleConfig['open-scap'].content) || !wodleConfig['open-scap']) &&
          !isString(currentConfig['wmodules-wmodules']) && (
            <WzNoConfig error="not-present" help={helpLinks} />
          )}
        {wodleConfig['open-scap'] && wodleConfig['open-scap'].content && (
          <WzConfigurationSettingsHeader
            title="Evaluations"
            description="Scans executed according to specific security policies and their profiles"
            help={helpLinks}
          >
            <EuiBasicTable
              columns={columns}
              items={wodleConfig['open-scap'].content}
            />
          </WzConfigurationSettingsHeader>
        )}
      </Fragment>
    );
  }
}

export default WzConfigurationOpenScapEvaluations;
