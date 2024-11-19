import {
  Xcyber360CorePluginStart,
  Xcyber360CorePluginSetup,
} from '../../xcyber360-core/server';

// eslint-disable-next-line @typescript-eslint/no-empty-interface
export interface AppPluginStartDependencies {}
// eslint-disable-next-line @typescript-eslint/no-empty-interface
export interface Xcyber360EnginePluginSetup {}
// eslint-disable-next-line @typescript-eslint/no-empty-interface
export interface Xcyber360EnginePluginStart {}

export type PluginSetup = {
  xcyber360Core: Xcyber360CorePluginSetup;
};

export interface AppPluginStartDependencies {
  xcyber360Core: Xcyber360CorePluginStart;
}
