/*
 * Xcyber360 app - React component for show configuration of OpenSCAP - general tab.
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

import WzConfigurationSettingsHeader from '../util-components/configuration-settings-header';
import WzConfigurationSettingsGroup from '../util-components/configuration-settings-group';
import WzNoConfig from '../util-components/no-config';
import helpLinks from './help-links';
import { isString, renderValueNoThenEnabled } from '../utils/utils';

const mainSettings = [
  {
    field: 'disabled',
    label: 'OpenSCAP integration status',
    render: renderValueNoThenEnabled
  },
  { field: 'timeout', label: 'Timeout (in seconds) for scan executions' },
  { field: 'interval', label: 'Interval between scan executions' },
  { field: 'scan-on-start', label: 'Scan on start' }
];

class WzConfigurationOpenSCAPGeneral extends Component {
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
          !wodleConfig['open-scap'] &&
          !isString(currentConfig['wmodules-wmodules']) && (
            <WzNoConfig error="not-present" help={helpLinks} />
          )}
        {wodleConfig['open-scap'] && (
          <WzConfigurationSettingsHeader
            title="Main settings"
            description="These settings apply to all OpenSCAP evaluations"
            help={helpLinks}
          >
            <WzConfigurationSettingsGroup
              config={wodleConfig['open-scap']}
              items={mainSettings}
            />
          </WzConfigurationSettingsHeader>
        )}
      </Fragment>
    );
  }
}

export default WzConfigurationOpenSCAPGeneral;
