import { PluginInitializer, PluginInitializerContext } from 'opensearch_dashboards/public';
import { Xcyber360Plugin } from './plugin';
import { Xcyber360Setup, Xcyber360SetupPlugins, Xcyber360Start, Xcyber360StartPlugins } from './types';

export const plugin: PluginInitializer<Xcyber360Setup, Xcyber360Start, Xcyber360SetupPlugins, Xcyber360StartPlugins> = (
  initializerContext: PluginInitializerContext
) => {
  return new Xcyber360Plugin(initializerContext);
};

// These are your public types & static code
export { Xcyber360Setup, Xcyber360Start };
