/*
 * Xcyber360 app
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

import { WzSecurityOpenSearchDashboardsSecurity } from './wz-security-opensearch-dashboards-security';

jest.mock('./generic-request', () => ({
  GenericRequest: {
    request: (method, path) => {
      return {
        data: {
          data: {
            xcyber360: {
              hash: '',
              reserved: true,
              hidden: false,
              backend_roles: ['admin'],
              attributes: {email: 'xcyber360@email.com', full_name: 'xcyber360 surname'},
              description: 'admin user',
              opendistro_security_roles: [],
              static: false,
            },
          },
        },
      };
    },
  },
}));
describe('Xcyber360 Internal Users', () => {
  it('Should return the ODFE internal users', async () => {
    const users = await WzSecurityOpenSearchDashboardsSecurity.getUsers();
    const expected_result = [
        { username: 'xcyber360', email: 'xcyber360@email.com', full_name: 'xcyber360 surname', roles: [] },
      ];
    expect(users).toEqual(expected_result);
  });
});
