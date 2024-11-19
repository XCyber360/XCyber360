import { PluginInitializerContext } from '../../../src/core/server';
import { Xcyber360CorePlugin } from './plugin';

// This exports static code and TypeScript types,
// as well as, OpenSearch Dashboards Platform `plugin()` initializer.

export function plugin(initializerContext: PluginInitializerContext) {
  return new Xcyber360CorePlugin(initializerContext);
}

export type { Xcyber360CorePluginSetup, Xcyber360CorePluginStart } from './types';
export type { IConfigurationEnhanced } from './services/enhance-configuration';
