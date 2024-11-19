import { AppMountParameters, CoreStart } from 'opensearch_dashboards/public';
import { ChartsPluginStart } from '../../../src/plugins/charts/public/plugin';
import { DiscoverStart } from '../../../src/plugins/discover/public';
import {
  VisualizationsSetup,
  VisualizationsStart,
} from '../../../src/plugins/visualizations/public';
import {
  DataPublicPluginSetup,
  DataPublicPluginStart,
} from '../../../src/plugins/data/public';
import { NavigationPublicPluginStart } from '../../../src/plugins/navigation/public';
import { UiActionsSetup } from '../../../src/plugins/ui_actions/public';
import { SecurityOssPluginStart } from '../../../src/plugins/security_oss/public/';
import { SavedObjectsStart } from '../../../src/plugins/saved_objects/public';
import {
  TelemetryPluginStart,
  TelemetryPluginSetup,
} from '../../../src/plugins/telemetry/public';
import { Xcyber360CheckUpdatesPluginStart } from '../../xcyber360-check-updates/public';
import { Xcyber360CorePluginStart } from '../../xcyber360-core/public';
import { Xcyber360EnginePluginStart } from '../../xcyber360-engine/public';
import { DashboardStart } from '../../../src/plugins/dashboard/public';
import { Xcyber360FleetPluginStart } from '../../xcyber360-fleet/public';

export interface AppPluginStartDependencies {
  navigation: NavigationPublicPluginStart;
  data: DataPublicPluginStart;
  visualizations: VisualizationsStart;
  discover: DiscoverStart;
  charts: ChartsPluginStart;
  securityOss: SecurityOssPluginStart;
  savedObjects: SavedObjectsStart;
  telemetry: TelemetryPluginStart;
  xcyber360CheckUpdates: Xcyber360CheckUpdatesPluginStart;
  xcyber360Core: Xcyber360CorePluginStart;
  xcyber360Engine: Xcyber360EnginePluginStart;
  dashboard: DashboardStart;
  xcyber360Fleet: Xcyber360FleetPluginStart;
}
export interface AppDependencies {
  core: CoreStart;
  plugins: AppPluginStartDependencies;
  params: AppMountParameters;
}

export type Xcyber360SetupPlugins = {
  uiActions: UiActionsSetup;
  visualizations: VisualizationsSetup;
  data: DataPublicPluginSetup;
  navigation: NavigationPublicPluginStart;
  telemetry: TelemetryPluginSetup;
};

export type Xcyber360StartPlugins = AppPluginStartDependencies;

export type Xcyber360Setup = {};
export type Xcyber360Start = {};
