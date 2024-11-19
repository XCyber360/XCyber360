import { CoreSetup, CoreStart, Plugin } from 'opensearch-dashboards/public';
import {
  AppPluginStartDependencies,
  Xcyber360EnginePluginSetup,
  Xcyber360EnginePluginStart,
} from './types';
import { setCore, setXcyber360Core } from './plugin-services';
import { Engine } from './components/engine';

export class Xcyber360EnginePlugin
  implements Plugin<Xcyber360EnginePluginSetup, Xcyber360EnginePluginStart>
{
  public setup(core: CoreSetup): Xcyber360EnginePluginSetup {
    return {};
  }

  public start(
    core: CoreStart,
    plugins: AppPluginStartDependencies,
  ): Xcyber360EnginePluginStart {
    setCore(core);
    setXcyber360Core(plugins.xcyber360Core);

    return { Engine };
  }

  public stop() {}
}
