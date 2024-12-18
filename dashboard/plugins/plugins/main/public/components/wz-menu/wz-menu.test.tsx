/*
 * Xcyber360 app - Health Check Component - Test
 *
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 *
 */

import React from 'react';
import { shallow } from 'enzyme';
import { WzMenu } from './wz-menu';


describe('WzMenu tests', () => {
  test('should render a WzMenu', () => {
    const component = shallow(<WzMenu />);

    expect(component).toMatchSnapshot();
  });
});