import {
  PluginInitializerContext,
  CoreSetup,
  CoreStart,
  Plugin,
  Logger,
} from 'opensearch-dashboards/server';

import {
  PluginSetup,
  Xcyber360CheckUpdatesPluginSetup,
  Xcyber360CheckUpdatesPluginStart,
  AppPluginStartDependencies,
} from './types';
import { defineRoutes } from './routes';
import {
  availableUpdatesObject,
  userPreferencesObject,
} from './services/saved-object/types';
import {
  setCore,
  setXcyber360Core,
  setInternalSavedObjectsClient,
  setXcyber360CheckUpdatesServices,
} from './plugin-services';
import { ISecurityFactory } from '../../xcyber360-core/server/services/security-factory';

declare module 'opensearch-dashboards/server' {
  interface RequestHandlerContext {
    xcyber360_check_updates: {
      logger: Logger;
      security: ISecurityFactory;
    };
  }
}

export class Xcyber360CheckUpdatesPlugin
  implements Plugin<Xcyber360CheckUpdatesPluginSetup, Xcyber360CheckUpdatesPluginStart>
{
  private readonly logger: Logger;

  constructor(initializerContext: PluginInitializerContext) {
    this.logger = initializerContext.logger.get();
  }

  public async setup(core: CoreSetup, plugins: PluginSetup) {
    this.logger.debug('xcyber360_check_updates: Setup');

    setXcyber360Core(plugins.xcyber360Core);
    setXcyber360CheckUpdatesServices({ logger: this.logger });

    core.http.registerRouteHandlerContext('xcyber360_check_updates', () => {
      return {
        logger: this.logger,
        security: plugins.xcyber360Core.dashboardSecurity,
      };
    });

    const router = core.http.createRouter();

    // Register saved objects types
    core.savedObjects.registerType(availableUpdatesObject);
    core.savedObjects.registerType(userPreferencesObject);

    // Register server side APIs
    defineRoutes(router);

    return {};
  }

  public start(
    core: CoreStart,
    plugins: AppPluginStartDependencies,
  ): Xcyber360CheckUpdatesPluginStart {
    this.logger.debug('xcyber360CheckUpdates: Started');

    const internalSavedObjectsClient =
      core.savedObjects.createInternalRepository();
    setCore(core);

    setInternalSavedObjectsClient(internalSavedObjectsClient);

    return {};
  }

  public stop() {}
}
