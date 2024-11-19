import { Xcyber360CorePlugin } from './plugin';

// This exports static code and TypeScript types,
// as well as, OpenSearch Dashboards Platform `plugin()` initializer.
export function plugin() {
  return new Xcyber360CorePlugin();
}
export { Xcyber360CorePluginSetup, Xcyber360CorePluginStart } from './types';
