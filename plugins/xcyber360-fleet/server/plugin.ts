import {
  PluginInitializerContext,
  CoreSetup,
  CoreStart,
  Plugin,
  Logger,
} from 'opensearch-dashboards/server';

import {
  PluginSetup,
  Xcyber360FleetPluginSetup,
  Xcyber360FleetPluginStart,
  AppPluginStartDependencies,
} from './types';

import {
  setCore,
  setXcyber360Core,
  setInternalSavedObjectsClient,
  setXcyber360FleetServices,
} from './plugin-services';
import { ISecurityFactory } from '../../xcyber360-core/server/services/security-factory';

declare module 'opensearch-dashboards/server' {
  interface RequestHandlerContext {
    xcyber360_fleet: {
      logger: Logger;
      security: ISecurityFactory;
    };
  }
}

export class Xcyber360FleetPlugin
  implements Plugin<Xcyber360FleetPluginSetup, Xcyber360FleetPluginStart>
{
  private readonly logger: Logger;

  constructor(initializerContext: PluginInitializerContext) {
    this.logger = initializerContext.logger.get();
  }

  public async setup(core: CoreSetup, plugins: PluginSetup) {
    this.logger.debug('xcyber360_fleet: Setup');

    setXcyber360Core(plugins.xcyber360Core);
    setXcyber360FleetServices({ logger: this.logger });

    core.http.registerRouteHandlerContext('xcyber360_fleet', () => {
      return {
        logger: this.logger,
        security: plugins.xcyber360Core.dashboardSecurity,
      };
    });

    return {};
  }

  public start(
    core: CoreStart,
    plugins: AppPluginStartDependencies,
  ): Xcyber360FleetPluginStart {
    this.logger.debug('xcyber360Fleet: Started');

    const internalSavedObjectsClient =
      core.savedObjects.createInternalRepository();
    setCore(core);

    setInternalSavedObjectsClient(internalSavedObjectsClient);

    return {};
  }

  public stop() {}
}
