import { PluginInitializerContext } from '../../../src/core/server';
import { Xcyber360FleetPlugin } from './plugin';

// This exports static code and TypeScript types,
// as well as, OpenSearch Dashboards Platform `plugin()` initializer.

export function plugin(initializerContext: PluginInitializerContext) {
  return new Xcyber360FleetPlugin(initializerContext);
}

export { Xcyber360FleetPluginSetup, Xcyber360FleetPluginStart } from './types';
