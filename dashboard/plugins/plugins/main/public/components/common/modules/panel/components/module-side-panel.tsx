/*
 * Xcyber360 app - React component ModuleSidePanel.
 *
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

import { EuiButtonEmpty, EuiCollapsibleNav } from '@elastic/eui';
import React, { useState } from 'react';
import './module-side-panel.scss';

export const ModuleSidePanel = ({ navIsDocked = false, children, ...props }) => {
  const [navIsOpen, setNavIsOpen] = useState(false);

  return (
    <EuiCollapsibleNav
      isOpen={navIsOpen}
      isDocked={navIsDocked}
      ownFocus={false}
      closeButtonPosition={'inside'}
      button={
        <EuiButtonEmpty
          className={'sidepanel-infoBtnStyle'}
          onClick={() => setNavIsOpen(!navIsOpen)}
          iconType={'iInCircle'}
        />
      }
      onClose={() => setNavIsOpen(false)}
    >
      <div>
        <div className={'wz-padding-16'}>{children}</div>
      </div>
    </EuiCollapsibleNav>
  );
};
