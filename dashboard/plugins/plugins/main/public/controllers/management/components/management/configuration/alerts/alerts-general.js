/*
 * Xcyber360 app - React component for show configuration of alerts - General tab.
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
import PropTypes from 'prop-types';

import WzConfigurationSettingsGroup from '../util-components/configuration-settings-group';
import WzConfigurationSettingsHeader from '../util-components/configuration-settings-header';
import WzNoConfig from '../util-components/no-config';
import { isString, renderValueOrNo } from '../utils/utils';
import { webDocumentationLink } from '../../../../../../../common/services/web_documentation';

const mainSettings = [
  {
    field: 'log_alert_level',
    label: 'Minimum severity level to store the alert',
  },
  {
    field: 'email_alert_level',
    label: 'Minimum severity level to send the alert by email',
  },
  {
    field: 'use_geoip',
    label: 'Enable GeoIP lookups',
    render: renderValueOrNo,
  },
];
const helpLinks = [
  {
    text: 'Use cases about alerts generation',
    href: webDocumentationLink('getting-started/use-cases/index.html'),
  },
  {
    text: 'Alerts reference',
    href: webDocumentationLink('user-manual/reference/ossec-conf/alerts.html'),
  },
];

class WzConfigurationAlertsGeneral extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    const { currentConfig, xcyber360NotReadyYet } = this.props;
    return (
      <Fragment>
        {currentConfig['analysis-alerts'] &&
          isString(currentConfig['analysis-alerts']) && (
            <WzNoConfig
              error={currentConfig['analysis-alerts']}
              help={helpLinks}
            />
          )}
        {currentConfig['analysis-alerts'] &&
          !isString(currentConfig['analysis-alerts']) &&
          !currentConfig['analysis-alerts'].alerts && (
            <WzNoConfig error='not-present' help={helpLinks} />
          )}
        {xcyber360NotReadyYet &&
          (!currentConfig || !currentConfig['analysis-alerts']) && (
            <WzNoConfig error='Server not ready yet' help={helpLinks} />
          )}
        {currentConfig['analysis-alerts'] &&
          !isString(currentConfig['analysis-alerts']) &&
          currentConfig['analysis-alerts'].alerts && (
            <WzConfigurationSettingsHeader
              title='Main settings'
              description='General alert settings'
              help={helpLinks}
            >
              <WzConfigurationSettingsGroup
                config={currentConfig['analysis-alerts'].alerts}
                items={mainSettings}
              />
            </WzConfigurationSettingsHeader>
          )}
      </Fragment>
    );
  }
}

WzConfigurationAlertsGeneral.propTypes = {
  xcyber360NotReadyYet: PropTypes.oneOfType([PropTypes.bool, PropTypes.string]),
};

export default WzConfigurationAlertsGeneral;
