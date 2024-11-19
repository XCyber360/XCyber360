import { Xcyber360CorePluginStart } from '../../xcyber360-core/public';
import { FleetManagementProps } from './components/fleet-management';
import { DashboardStart } from '../../../src/plugins/dashboard/public';

export interface Xcyber360FleetPluginSetup {}
// eslint-disable-next-line @typescript-eslint/no-empty-interface
export interface Xcyber360FleetPluginStart {
  FleetManagement: (props: FleetManagementProps) => JSX.Element;
}

export interface AppPluginStartDependencies {
  xcyber360Core: Xcyber360CorePluginStart;
  dashboard: DashboardStart;
}
