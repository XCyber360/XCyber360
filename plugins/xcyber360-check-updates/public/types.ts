import { Xcyber360CorePluginStart } from '../../xcyber360-core/public';
import { AvailableUpdates } from '../common/types';

export interface Xcyber360CheckUpdatesPluginSetup {}
// eslint-disable-next-line @typescript-eslint/no-empty-interface
export interface Xcyber360CheckUpdatesPluginStart {
  UpdatesNotification: () => JSX.Element | null;
  getAvailableUpdates: (
    queryApi: boolean,
    forceQuery: boolean,
  ) => Promise<AvailableUpdates>;
  DismissNotificationCheck: () => JSX.Element | null;
}

export interface AppPluginStartDependencies {
  xcyber360Core: Xcyber360CorePluginStart;
}
