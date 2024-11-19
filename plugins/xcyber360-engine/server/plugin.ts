import {
  PluginInitializerContext,
  CoreSetup,
  CoreStart,
  Plugin,
  Logger,
} from 'opensearch-dashboards/server';

import {
  PluginSetup,
  Xcyber360EnginePluginSetup,
  Xcyber360EnginePluginStart,
  AppPluginStartDependencies,
} from './types';
import { defineRoutes } from './routes';
import { setCore, setXcyber360Core } from './plugin-services';
import { ISecurityFactory } from '../../xcyber360-core/server/services/security-factory';

declare module 'opensearch-dashboards/server' {
  interface RequestHandlerContext {
    xcyber360_check_updates: {
      logger: Logger;
      security: ISecurityFactory;
    };
  }
}

export class Xcyber360EnginePlugin
  implements Plugin<Xcyber360EnginePluginSetup, Xcyber360EnginePluginStart>
{
  private readonly logger: Logger;

  constructor(initializerContext: PluginInitializerContext) {
    this.logger = initializerContext.logger.get();
  }

  public async setup(core: CoreSetup, plugins: PluginSetup) {
    this.logger.debug('Setup');

    setXcyber360Core(plugins.xcyber360Core);

    core.http.registerRouteHandlerContext('xcyber360_engine', () => {
      return {
        logger: this.logger,
      };
    });

    const router = core.http.createRouter();

    // Register server side APIs
    defineRoutes(router);

    return {};
  }

  public start(
    core: CoreStart,
    plugins: AppPluginStartDependencies,
  ): Xcyber360EnginePluginStart {
    this.logger.debug('Started');
    setCore(core);

    return {};
  }

  public stop() {}
}
