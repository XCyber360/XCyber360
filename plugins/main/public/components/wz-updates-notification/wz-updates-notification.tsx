/*
 * Xcyber360 app - React Component component to display new updates notification.
 *
 * Copyright (C) 2015-2023 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

import React from 'react';
import { connect } from 'react-redux';
import { getXcyber360CheckUpdatesPlugin } from '../../kibana-services';

const mapStateToProps = state => {
  return {
    appConfig: state?.appConfig,
  };
};
export const WzUpdatesNotification = connect(mapStateToProps)(
  ({ appConfig }) => {
    const isUpdatesEnabled =
      !appConfig?.isLoading && !appConfig?.data?.['xcyber360.updates.disabled'];
    const { UpdatesNotification } = getXcyber360CheckUpdatesPlugin();

    return isUpdatesEnabled ? <UpdatesNotification /> : <></>;
  },
);
