import { IRouter } from 'opensearch_dashboards/server';
import { Xcyber360ApiRoutes } from './xcyber360-api';
import { Xcyber360ElasticRoutes } from './xcyber360-elastic';
import { Xcyber360HostsRoutes } from './xcyber360-hosts';
import { Xcyber360UtilsRoutes, UiLogsRoutes } from './xcyber360-utils';
import { Xcyber360ReportingRoutes } from './xcyber360-reporting';

export const setupRoutes = (router: IRouter, services) => {
  Xcyber360ApiRoutes(router, services);
  Xcyber360ElasticRoutes(router, services);
  Xcyber360HostsRoutes(router, services);
  Xcyber360UtilsRoutes(router, services);
  Xcyber360ReportingRoutes(router, services);
  UiLogsRoutes(router, services);
};
