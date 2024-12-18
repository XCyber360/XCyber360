/*
 * Xcyber360 app - React component for show configuration of log collection - commands tab.
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

import WzNoConfig from '../util-components/no-config';
import WzConfigurationSettingsHeader from '../util-components/configuration-settings-header';
import WzConfigurationListSelector from '../util-components/configuration-settings-list-selector';
import { renderValueOrNoValue, isString } from '../utils/utils';
import { settingsListBuilder } from '../utils/builders';
import helpLinks from './help-links';
import { LOGCOLLECTOR_LOCALFILE_PROP, LOCALFILE_WINDOWSEVENT_PROP } from './types';

/**
 *  Return input label based on logformat value
 *
 * @param {*} value => field value
 * @param {*} item => settings item
 * @param {*} config => all log data
 * @returns string => value to show in Channel label
 */
const channelLabel = (value, item, config) => {
  return config.logformat === 'eventlog'
    ? 'Log'
    : config.logformat === 'eventchannel'
    ? 'Channel'
    : 'Channel';
};

/**
 *
 * @param {*} data => all log data
 * @returns string => value to show in query input
 */
const queryValue = (data) => {
  return typeof data === 'undefined' ? '-' : typeof data === 'object' ? data.value : data;
};

/**
 * Returns targets array parsed in one string
 * @param {*} item
 * @returns string => target
 */
const renderTargetField = (item) => (item ? item.join(', ') : 'agent');
/**
 * Return panels title
 * @param {*} item => log data
 * @returns
 */
const panelsLabel = (item) =>
  !item.channel
    ? `${item.logformat} - ${renderTargetField(item.target)}`
    : `${item.channel} (${item.logformat})`;

const mainSettings = [
  { field: 'logformat', label: 'Log format' },
  { field: 'channel', label: 'Channel', render: renderValueOrNoValue, renderLabel: channelLabel },
  { field: 'query', label: 'Query', render: queryValue },
  {
    field: 'only-future-events',
    label: 'Only future events',
    render: renderValueOrNoValue,
  },
  {
    field: 'reconnect_time',
    label: 'Reconnect Time',
    render: renderValueOrNoValue,
  },
];

class WzConfigurationLogCollectionWindowsEvents extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    const { currentConfig } = this.props;
    const items = currentConfig?.[LOGCOLLECTOR_LOCALFILE_PROP]?.[LOCALFILE_WINDOWSEVENT_PROP]
      ? settingsListBuilder(
          currentConfig[LOGCOLLECTOR_LOCALFILE_PROP][LOCALFILE_WINDOWSEVENT_PROP],
          panelsLabel
        )
      : [];
    return (
      <Fragment>
        {isString(currentConfig?.[LOGCOLLECTOR_LOCALFILE_PROP]) && (
          <WzNoConfig error={currentConfig[LOGCOLLECTOR_LOCALFILE_PROP]} help={helpLinks} />
        )}
        {!currentConfig?.[LOGCOLLECTOR_LOCALFILE_PROP]?.[LOCALFILE_WINDOWSEVENT_PROP]?.length ? (
          <WzNoConfig error="not-present" help={helpLinks} />
        ) : null}
        {currentConfig?.[LOGCOLLECTOR_LOCALFILE_PROP]?.[LOCALFILE_WINDOWSEVENT_PROP]?.length ? (
          <WzConfigurationSettingsHeader
            title="Windows events logs"
            description="List of Windows logs that will be processed"
            help={helpLinks}
          >
            <WzConfigurationListSelector items={items} settings={mainSettings} />
          </WzConfigurationSettingsHeader>
        ) : null}
      </Fragment>
    );
  }
}

export default WzConfigurationLogCollectionWindowsEvents;
