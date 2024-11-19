import { Xcyber360CorePluginStart } from '../../xcyber360-core/public';

export interface Xcyber360EnginePluginSetup {}
// eslint-disable-next-line @typescript-eslint/no-empty-interface
export interface Xcyber360EnginePluginStart {}

export interface AppPluginStartDependencies {
  xcyber360Core: Xcyber360CorePluginStart;
}
