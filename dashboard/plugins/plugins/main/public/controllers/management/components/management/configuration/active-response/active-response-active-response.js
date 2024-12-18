/*
 * Xcyber360 app - React component for show configuration of active response - active response tab.
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

import WzNoConfig from '../util-components/no-config';
import WzConfigurationSettingsHeader from '../util-components/configuration-settings-header';
import WzConfigurationSettingsListSelector from '../util-components/configuration-settings-list-selector';
import { isString, renderValueNoThenEnabled } from '../utils/utils';
import { settingsListBuilder } from '../utils/builders';

import { connect } from 'react-redux';
import { compose } from 'redux';

import withWzConfig from '../util-hocs/wz-config';
import { webDocumentationLink } from '../../../../../../../common/services/web_documentation';

const mainSettings = [
  { field: 'command', label: 'Command to execute' },
  { field: 'location', label: 'Execute the command on this location' },
  { field: 'agent_id', label: 'Agent ID on which execute the command' },
  { field: 'level', label: 'Match to this severity level or above' },
  { field: 'rules_group', label: 'Match to one of these groups' },
  { field: 'rules_id', label: 'Match to one of these rule IDs' },
  { field: 'timeout', label: 'Timeout (in seconds) before reverting' },
];

const helpLinks = [
  {
    text: 'Active response documentation',
    href: webDocumentationLink(
      'user-manual/capabilities/active-response/index.html',
    ),
  },
  {
    text: 'Active response reference',
    href: webDocumentationLink(
      'user-manual/reference/ossec-conf/active-response.html',
    ),
  },
];

class WzConfigurationActiveResponseActiveResponse extends Component {
  constructor(props) {
    super(props);
  }
  render() {
    const { currentConfig, xcyber360NotReadyYet } = this.props;
    const items =
      !isString(currentConfig['analysis-active_response']) &&
      currentConfig['analysis-active_response']['active-response'] &&
      currentConfig['analysis-active_response']['active-response'].length
        ? settingsListBuilder(
            currentConfig['analysis-active_response']['active-response'],
            'command',
          )
        : [];
    return (
      <Fragment>
        {currentConfig['analysis-active_response'] &&
          isString(currentConfig['analysis-active_response']) && (
            <WzNoConfig
              error={currentConfig['analysis-active_response']}
              help={helpLinks}
            />
          )}
        {currentConfig['analysis-active_response'] &&
          !isString(currentConfig['analysis-active_response']) &&
          currentConfig['analysis-active_response']['active-response'] &&
          !currentConfig['analysis-active_response']['active-response']
            .length && <WzNoConfig error='not-present' help={helpLinks} />}
        {xcyber360NotReadyYet &&
          (!currentConfig || !currentConfig['analysis-active_response']) && (
            <WzNoConfig error='Server not ready yet' help={helpLinks} />
          )}
        {currentConfig['analysis-active_response'] &&
        !isString(currentConfig['analysis-active_response']) &&
        currentConfig['analysis-active_response']['active-response'].length ? (
          <WzConfigurationSettingsHeader
            title='Active response definitions'
            description="Find here all the currently defined active responses. Disabled active responses don't show up."
            help={helpLinks}
          >
            <WzConfigurationSettingsListSelector
              items={items}
              settings={mainSettings}
            />
          </WzConfigurationSettingsHeader>
        ) : null}
      </Fragment>
    );
  }
}

WzConfigurationActiveResponseActiveResponse.propTypes = {
  // currentConfig: PropTypes.object.isRequired,
  xcyber360NotReadyYet: PropTypes.oneOfType([PropTypes.bool, PropTypes.string]),
};

const mapStateToProps = state => ({
  xcyber360NotReadyYet: state.appStateReducers.xcyber360NotReadyYet,
});

export default connect(mapStateToProps)(
  WzConfigurationActiveResponseActiveResponse,
);

const sectionsAgent = [{ component: 'com', configuration: 'active-response' }];

export const WzConfigurationActiveResponseActiveResponseAgent = compose(
  connect(mapStateToProps),
  withWzConfig(sectionsAgent),
)(WzConfigurationActiveResponseActiveResponse);

WzConfigurationActiveResponseActiveResponseAgent.propTypes = {
  xcyber360NotReadyYet: PropTypes.oneOfType([PropTypes.bool, PropTypes.string]),
};
