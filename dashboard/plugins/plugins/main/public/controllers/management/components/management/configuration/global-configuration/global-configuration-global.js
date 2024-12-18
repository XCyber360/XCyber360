/*
 * Xcyber360 app - React component for show configuration of global configuration - global tab.
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

import { isString } from '../utils/utils';
import { webDocumentationLink } from '../../../../../../../common/services/web_documentation';

const helpLinks = [
  {
    text: 'Global reference',
    href: webDocumentationLink('user-manual/reference/ossec-conf/global.html'),
  },
  {
    text: 'Logging reference',
    href: webDocumentationLink('user-manual/reference/ossec-conf/logging.html'),
  },
];

const mainSettings = [
  { field: 'alerts_log', label: 'Write alerts to alerts.log file' },
  {
    field: 'jsonout_output',
    label: 'Write JSON formatted alerts to alerts.json file',
  },
  { field: 'logall', label: 'Archive all the alerts in plain text format' },
  { field: 'logall_json', label: 'Archive all the alerts in JSON format' },
  {
    field: 'custom_alert_output',
    label: 'Customized alerts format for alerts.log file',
  },
  { field: 'plain', label: 'Write internal logs in plain text' },
  { field: 'json', label: 'Write internal logs in JSON format' },
  { field: 'max_output_size', label: 'Size limit of alert files' },
  { field: 'rotate_interval', label: 'File rotation interval' },
];

const emailSettings = [
  { field: 'email_notification', label: 'Enable alerts sent by email' },
  { field: 'email_from', label: 'Sender adress for email alerts' },
  { field: 'email_to', label: 'Recipient address for email alerts' },
  { field: 'email_reply_to', label: 'Reply-to address for email alerts' },
  { field: 'smtp_server', label: 'Address for SMTP mail server' },
  {
    field: 'email_maxperhour',
    label: 'Maximum number of email alerts sent per hour',
  },
  { field: 'email_log_source', label: 'File to read data from' },
  { field: 'email_idsname', label: 'Name used for email alerts headers' },
];

const otherSettings = [
  {
    field: 'stats',
    label: 'Severity level for alerts generated by statistical analysis',
  },
  {
    field: 'host_information',
    label: 'Severity level for alerts generated by host change monitor',
  },
  {
    field: 'memory_size',
    label: 'Memory size for the alert correlation engine',
  },
  { field: 'white_list', label: 'White-listed IP addresses' },
  {
    field: 'geoip_db_path',
    label: 'Full path to MaxMind GeoIP IPv4 database file',
  },
];

const preludeZeroMQOutputSettings = [
  { field: 'prelude_output', label: 'Enable Prelude output' },
  { field: 'zeromq_output', label: 'Enable ZeroMQ output' },
  { field: 'zeromq_uri', label: 'ZeroMQ URI to bind publisher socket' },
];

const buildHelpLinks = agent =>
  agent.id === '000' ? helpLinks : [helpLinks[1]];

class WzConfigurationGlobalConfigurationGlobal extends Component {
  constructor(props) {
    super(props);
    this.helpLinks = buildHelpLinks(this.props.agent);
  }
  render() {
    const { currentConfig, agent, xcyber360NotReadyYet } = this.props;
    const mainSettingsConfig =
      agent.id === '000' &&
      currentConfig['analysis-global'] &&
      currentConfig['analysis-global'].global &&
      currentConfig['com-logging'] &&
      currentConfig['com-logging'].logging
        ? {
            ...currentConfig['analysis-global'].global,
            plain: currentConfig['com-logging'].logging.plain,
            json: currentConfig['com-logging'].logging.json,
          }
        : currentConfig['com-logging'] && currentConfig['com-logging'].logging
        ? {
            plain: currentConfig['com-logging'].logging.plain,
            json: currentConfig['com-logging'].logging.json,
          }
        : {};
    const globalSettingsConfig =
      agent.id === '000' &&
      currentConfig['analysis-global'] &&
      currentConfig['analysis-global'].global
        ? {
            ...currentConfig['analysis-global'].global,
          }
        : {};
    return (
      <Fragment>
        {currentConfig['analysis-global'] &&
          isString(currentConfig['analysis-global']) && (
            <WzNoConfig
              error={currentConfig['analysis-global']}
              help={this.helpLinks}
            />
          )}
        {agent &&
          agent.id !== '000' &&
          currentConfig['com-logging'] &&
          isString(currentConfig['com-logging']) && (
            <WzNoConfig
              error={currentConfig['com-global']}
              help={this.helpLinks}
            />
          )}
        {currentConfig['analysis-global'] &&
          !isString(currentConfig['analysis-global']) &&
          !currentConfig['analysis-global'].global && (
            <WzNoConfig error='not-present' help={this.helpLinks} />
          )}
        {xcyber360NotReadyYet &&
          (!currentConfig || !currentConfig['analysis-global']) && (
            <WzNoConfig error='Server not ready yet' help={this.helpLinks} />
          )}
        {((currentConfig['analysis-global'] &&
          currentConfig['analysis-global'].global) ||
          (currentConfig['com-logging'] &&
            currentConfig['com-logging'].logging)) && (
          <WzConfigurationSettingsHeader
            title='Main settings'
            description='Basic alerts and logging settings'
            help={this.helpLinks}
          >
            <WzConfigurationSettingsGroup
              config={mainSettingsConfig}
              items={mainSettings}
            />
            {agent.id === '000' && (
              <Fragment>
                <WzConfigurationSettingsGroup
                  title='Email settings'
                  description='Basic email settings (needed for granular email settings)'
                  config={globalSettingsConfig}
                  items={emailSettings}
                />
                <WzConfigurationSettingsGroup
                  title='Other settings'
                  description='Settings not directly related to any specific component'
                  config={globalSettingsConfig}
                  items={otherSettings}
                />
                <WzConfigurationSettingsGroup
                  title='Prelude and ZeroMQ output'
                  config={globalSettingsConfig}
                  items={preludeZeroMQOutputSettings}
                />
              </Fragment>
            )}
          </WzConfigurationSettingsHeader>
        )}
      </Fragment>
    );
  }
}

WzConfigurationGlobalConfigurationGlobal.propTypes = {
  agent: PropTypes.object,
  xcyber360NotReadyYet: PropTypes.oneOfType([PropTypes.bool, PropTypes.string]),
};

export default WzConfigurationGlobalConfigurationGlobal;
