import { PluginInitializerContext } from 'opensearch_dashboards/server';

import { Xcyber360Plugin } from './plugin';

//  This exports static code and TypeScript types,
//  as well as, plugin platform `plugin()` initializer.

export function plugin(initializerContext: PluginInitializerContext) {
  return new Xcyber360Plugin(initializerContext);
}

export { Xcyber360PluginSetup, Xcyber360PluginStart } from './types';
