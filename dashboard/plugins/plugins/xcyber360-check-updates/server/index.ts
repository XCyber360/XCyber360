import { PluginInitializerContext } from '../../../src/core/server';
import { Xcyber360CheckUpdatesPlugin } from './plugin';

// This exports static code and TypeScript types,
// as well as, OpenSearch Dashboards Platform `plugin()` initializer.

export function plugin(initializerContext: PluginInitializerContext) {
  return new Xcyber360CheckUpdatesPlugin(initializerContext);
}

export { Xcyber360CheckUpdatesPluginSetup, Xcyber360CheckUpdatesPluginStart } from './types';
