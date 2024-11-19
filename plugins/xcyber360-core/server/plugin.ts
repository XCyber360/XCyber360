import {
  PluginInitializerContext,
  CoreSetup,
  CoreStart,
  Plugin,
  Logger,
} from 'opensearch-dashboards/server';
import { validate as validateNodeCronInterval } from 'node-cron';
import {
  PluginSetup,
  Xcyber360CorePluginSetup,
  Xcyber360CorePluginStart,
} from './types';
import { setCore } from './plugin-services';
import {
  ManageHosts,
  createDashboardSecurity,
  ServerAPIClient,
  UpdateRegistry,
  ConfigurationStore,
} from './services';
import { Configuration } from '../common/services/configuration';
import {
  PLUGIN_SETTINGS,
  PLUGIN_SETTINGS_CATEGORIES,
  XCYBER360_CORE_CONFIGURATION_CACHE_SECONDS,
  XCYBER360_DATA_CONFIG_APP_PATH,
} from '../common/constants';
import { enhanceConfiguration } from './services/enhance-configuration';

export class Xcyber360CorePlugin
  implements Plugin<Xcyber360CorePluginSetup, Xcyber360CorePluginStart>
{
  private readonly logger: Logger;
  private services: { [key: string]: any };
  private _internal: { [key: string]: any };

  constructor(private initializerContext: PluginInitializerContext) {
    this.logger = initializerContext.logger.get();
    this.services = {};
    this._internal = {};
  }

  public async setup(
    core: CoreSetup,
    plugins: PluginSetup,
  ): Promise<Xcyber360CorePluginSetup> {
    this.logger.debug('xcyber360_core: Setup');

    this.services.dashboardSecurity = createDashboardSecurity(plugins);

    this._internal.configurationStore = new ConfigurationStore(
      this.logger.get('configuration-store'),
      {
        cache_seconds: XCYBER360_CORE_CONFIGURATION_CACHE_SECONDS,
        file: XCYBER360_DATA_CONFIG_APP_PATH,
      },
    );
    this.services.configuration = new Configuration(
      this.logger.get('configuration'),
      this._internal.configurationStore,
    );

    // Enhance configuration service
    enhanceConfiguration(this.services.configuration);

    // Register the plugin settings
    Object.entries(PLUGIN_SETTINGS).forEach(([key, value]) =>
      this.services.configuration.register(key, value),
    );

    // Add categories to the configuration
    Object.entries(PLUGIN_SETTINGS_CATEGORIES).forEach(([key, value]) => {
      this.services.configuration.registerCategory({ ...value, id: key });
    });

    /* Workaround: Redefine the validation functions of cron.statistics.interval setting.
      Because the settings are defined in the backend and frontend side using the same definitions,
      the validation funtions are not defined there and has to be defined in the frontend side and backend side
      */
    const setting = this.services.configuration._settings.get(
      'cron.statistics.interval',
    );
    !setting.validateUIForm &&
      (setting.validateUIForm = function (value) {
        return this.validate(value);
      });
    !setting.validate &&
      (setting.validate = function (value: string) {
        return validateNodeCronInterval(value)
          ? undefined
          : 'Interval is not valid.';
      });

    this.services.configuration.setup();

    this.services.manageHosts = new ManageHosts(
      this.logger.get('manage-hosts'),
      this.services.configuration,
    );

    this.services.serverAPIClient = new ServerAPIClient(
      this.logger.get('server-api-client'),
      this.services.manageHosts,
      this.services.dashboardSecurity,
    );

    this.services.manageHosts.setServerAPIClient(this.services.serverAPIClient);

    // Register a property to the context parameter of the endpoint handlers
    core.http.registerRouteHandlerContext('xcyber360_core', (context, request) => {
      return {
        ...this.services,
        api: {
          client: {
            asInternalUser: this.services.serverAPIClient.asInternalUser,
            asCurrentUser: this.services.serverAPIClient.asScoped(
              context,
              request,
            ),
          },
        },
      };
    });

    return {
      ...this.services,
      api: {
        client: {
          asInternalUser: this.services.serverAPIClient.asInternalUser,
          asScoped: this.services.serverAPIClient.asScoped,
        },
      },
    };
  }

  public async start(core: CoreStart): Promise<Xcyber360CorePluginStart> {
    this.logger.debug('xcyber360Core: Started');

    setCore(core);

    await this.services.configuration.start();
    await this.services.manageHosts.start();

    return {
      ...this.services,
      api: {
        client: {
          asInternalUser: this.services.serverAPIClient.asInternalUser,
          asScoped: this.services.serverAPIClient.asScoped,
        },
      },
    };
  }

  public stop() {}
}
