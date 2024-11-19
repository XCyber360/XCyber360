import { PluginInitializerContext } from '../../../src/core/server';
import { Xcyber360EnginePlugin } from './plugin';

// This exports static code and TypeScript types,
// as well as, OpenSearch Dashboards Platform `plugin()` initializer.

export function plugin(initializerContext: PluginInitializerContext) {
  return new Xcyber360EnginePlugin(initializerContext);
}

export type { Xcyber360EnginePluginSetup, Xcyber360EnginePluginStart } from './types';
