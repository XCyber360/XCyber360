/*
 * Xcyber360 app - React component GeneralTab
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

import React from 'react';

import { renderValueYesThenEnabled } from '../../../utils/utils';
import WzConfigurationSettingsHeader from '../../../util-components/configuration-settings-header';
import WzConfigurationSettingsGroup from '../../../util-components/configuration-settings-group';
import { HELP_LINKS, OFFICE_365 } from '../../constants';

export type GeneralTableProps = {
  agent: { id: string };
  wodleConfiguration: any;
};

const mainSettings = [
  {
    field: 'enabled',
    label: 'Service status',
    render: renderValueYesThenEnabled,
  },
  {
    field: 'only_future_events',
    label: 'Collect events generated since manager is initialized',
  },
  {
    field: 'interval',
    label: 'Interval between Office 365 wodle executions in seconds',
  },
  {
    field: 'curl_max_size',
    label: 'Maximum size allowed for the Office 365 API response',
  },
];

export const GeneralTab = ({
  agent,
  wodleConfiguration,
}: GeneralTableProps) => {
  return (
    <WzConfigurationSettingsHeader
      title='Main settings'
      description='Configuration for the Office 365 module'
      help={HELP_LINKS}
    >
      <WzConfigurationSettingsGroup
        config={wodleConfiguration[OFFICE_365]}
        items={mainSettings}
      />
    </WzConfigurationSettingsHeader>
  );
};
