import { Xcyber360FleetPlugin } from './plugin';

// This exports static code and TypeScript types,
// as well as, OpenSearch Dashboards Platform `plugin()` initializer.
export function plugin() {
  return new Xcyber360FleetPlugin();
}
export { Xcyber360FleetPluginSetup, Xcyber360FleetPluginStart } from './types';
