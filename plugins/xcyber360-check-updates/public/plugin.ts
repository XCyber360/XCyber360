import { CoreSetup, CoreStart, Plugin } from 'opensearch-dashboards/public';
import {
  AppPluginStartDependencies,
  Xcyber360CheckUpdatesPluginSetup,
  Xcyber360CheckUpdatesPluginStart,
} from './types';
import { UpdatesNotification } from './components/updates-notification';
import { DismissNotificationCheck } from './components/dismiss-notification-check';
import { setCore, setXcyber360Core } from './plugin-services';
import { getAvailableUpdates } from './services';

export class Xcyber360CheckUpdatesPlugin
  implements Plugin<Xcyber360CheckUpdatesPluginSetup, Xcyber360CheckUpdatesPluginStart> {
  public setup(core: CoreSetup): Xcyber360CheckUpdatesPluginSetup {
    return {};
  }

  public start(core: CoreStart, plugins: AppPluginStartDependencies): Xcyber360CheckUpdatesPluginStart {
    setCore(core);
    setXcyber360Core(plugins.xcyber360Core);

    return {
      UpdatesNotification,
      getAvailableUpdates,
      DismissNotificationCheck,
    };
  }

  public stop() {}
}
