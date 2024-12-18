/*
 * Xcyber360 app - Integrity monitoring components
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

import React, { Component } from 'react';
import { Mitre } from '../../../components/overview';
import { withUserAuthorizationPrompt, withAgentSupportModule } from '../hocs';
import { compose } from 'redux';

export const MainMitre = compose(
  withAgentSupportModule,
  withUserAuthorizationPrompt([{ action: 'mitre:read', resource: '*:*:*' }]),
)(
  class MainMitre extends Component {
    constructor(props) {
      super(props);
    }

    render() {
      return <Mitre {...this.props} />;
    }
  },
);
