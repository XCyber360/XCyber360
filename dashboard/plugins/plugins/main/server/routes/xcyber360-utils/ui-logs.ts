/*
 * Xcyber360 app - Module for UI Logs routes
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */
import { UiLogsCtrl } from '../../controllers';
import { IRouter } from 'opensearch_dashboards/server';
import { schema } from '@osd/config-schema';

export const UiLogsRoutes = (router: IRouter) => {
  const ctrl = new UiLogsCtrl();

  router.post(
    {
      path: '/utils/logs/ui',
      validate: {
        body: schema.object({
          message: schema.string(),
          level: schema.string(),
          location: schema.string(),
        }),
      },
    },
    async (context, request, response) =>
      await ctrl.createUiLogs(context, request, response),
  );
};
