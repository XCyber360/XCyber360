import { ISecurityFactory } from '../../xcyber360-core/server/services/security-factory';
import { Xcyber360CorePluginStart } from '../../xcyber360-core/server';

// eslint-disable-next-line @typescript-eslint/no-empty-interface
export interface AppPluginStartDependencies {}
// eslint-disable-next-line @typescript-eslint/no-empty-interface
export interface Xcyber360CheckUpdatesPluginSetup {}
// eslint-disable-next-line @typescript-eslint/no-empty-interface
export interface Xcyber360CheckUpdatesPluginStart {}

export type PluginSetup = {
  securityDashboards?: {}; // TODO: Add OpenSearch Dashboards Security interface
  xcyber360Core: { dashboardSecurity: ISecurityFactory };
};

export interface AppPluginStartDependencies {
  xcyber360Core: Xcyber360CorePluginStart;
}
