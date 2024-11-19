import { CoreSetup, CoreStart, Plugin } from 'opensearch-dashboards/public';
import {
  AppPluginStartDependencies,
  Xcyber360FleetPluginSetup,
  Xcyber360FleetPluginStart,
} from './types';
import { FleetManagement } from './components';
import { setCore, setPlugins, setXcyber360Core } from './plugin-services';

export class Xcyber360FleetPlugin
  implements Plugin<Xcyber360FleetPluginSetup, Xcyber360FleetPluginStart>
{
  public setup(core: CoreSetup): Xcyber360FleetPluginSetup {
    return {};
  }

  public start(
    core: CoreStart,
    plugins: AppPluginStartDependencies,
  ): Xcyber360FleetPluginStart {
    setCore(core);
    setPlugins(plugins);
    setXcyber360Core(plugins.xcyber360Core);

    return {
      FleetManagement,
    };
  }

  public stop() {}
}
