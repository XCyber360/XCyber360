/*
 * Xcyber360 app - Update allow_run_as Service
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

import { User } from '../types/user.type';
import { WzRequest } from '../../../../react-services/wz-request';
import IApiResponse from '../../../../react-services/interfaces/api-response.interface';

const UpdateAllowRunAsService = async (userId: number, allowRunAs: boolean = false): Promise<User> => {
  const response = (await WzRequest.apiReq(
    'PUT',
    `/security/users/${userId}/run_as?allow_run_as=${allowRunAs}`,
    {}
  )) as IApiResponse<User>;
  const users = ((response.data || {}).data || {}).affected_items || [{}];
  return users[0];
};

export default UpdateAllowRunAsService;
