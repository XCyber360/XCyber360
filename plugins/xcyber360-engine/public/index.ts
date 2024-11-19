import { Xcyber360EnginePlugin } from './plugin';

// This exports static code and TypeScript types,
// as well as, OpenSearch Dashboards Platform `plugin()` initializer.
export function plugin() {
  return new Xcyber360EnginePlugin();
}
export type { Xcyber360EnginePluginSetup, Xcyber360EnginePluginStart } from './types';
