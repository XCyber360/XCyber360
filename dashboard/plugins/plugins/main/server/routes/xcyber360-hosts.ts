/*
 * Xcyber360 app - Module for Xcyber360-API routes
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */
import { Xcyber360HostsCtrl } from '../controllers';
import { IRouter } from 'opensearch_dashboards/server';

export function Xcyber360HostsRoutes(router: IRouter, services) {
  const ctrl = new Xcyber360HostsCtrl();

  // Get Xcyber360-API entries list (Multimanager) from elasticsearch index
  router.get(
    {
      path: '/hosts/apis',
      validate: false,
    },
    async (context, request, response) =>
      ctrl.getHostsEntries(context, request, response),
  );
}
