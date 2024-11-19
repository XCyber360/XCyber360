import {
  ChromeStart,
  CoreStart,
  HttpStart,
  IUiSettingsClient,
  OverlayStart,
  SavedObjectsStart,
  ScopedHistory,
  ToastsStart,
  AppMountParameters,
} from 'opensearch_dashboards/public';
import { createGetterSetter } from '../../../src/plugins/opensearch_dashboards_utils/common';
import { DataPublicPluginStart } from '../../../src/plugins/data/public';
import { VisualizationsStart } from '../../../src/plugins/visualizations/public';
import { NavigationPublicPluginStart } from '../../../src/plugins/navigation/public';
import { AppPluginStartDependencies } from './types';
import { Xcyber360CheckUpdatesPluginStart } from '../../xcyber360-check-updates/public';
import { Xcyber360EnginePluginStart } from '../../xcyber360-engine/public';
import { Xcyber360FleetPluginStart } from '../../xcyber360-fleet/public';

let angularModule: any = null;
let discoverModule: any = null;

export const [getCore, setCore] = createGetterSetter<CoreStart>('Core');
export const [getPlugins, setPlugins] =
  createGetterSetter<AppPluginStartDependencies>('Plugins');
export const [getToasts, setToasts] = createGetterSetter<ToastsStart>('Toasts');
export const [getHttp, setHttp] = createGetterSetter<HttpStart>('Http');
export const [getUiSettings, setUiSettings] =
  createGetterSetter<IUiSettingsClient>('UiSettings');
export const [getChrome, setChrome] = createGetterSetter<ChromeStart>('Chrome');
export const [getScopedHistory, setScopedHistory] =
  createGetterSetter<ScopedHistory>('ScopedHistory');
export const [getOverlays, setOverlays] =
  createGetterSetter<OverlayStart>('Overlays');
export const [getSavedObjects, setSavedObjects] =
  createGetterSetter<SavedObjectsStart>('SavedObjects');
export const [getDataPlugin, setDataPlugin] =
  createGetterSetter<DataPublicPluginStart>('DataPlugin');
export const [getVisualizationsPlugin, setVisualizationsPlugin] =
  createGetterSetter<VisualizationsStart>('VisualizationsPlugin');
export const [getNavigationPlugin, setNavigationPlugin] =
  createGetterSetter<NavigationPublicPluginStart>('NavigationPlugin');
export const [getWzMainParams, setWzMainParams] =
  createGetterSetter<NavigationPublicPluginStart>('WzMainParams');
export const [getWzCurrentAppID, setWzCurrentAppID] =
  createGetterSetter<NavigationPublicPluginStart>('WzCurrentAppID');
export const [getXcyber360CheckUpdatesPlugin, setXcyber360CheckUpdatesPlugin] =
  createGetterSetter<Xcyber360CheckUpdatesPluginStart>('Xcyber360CheckUpdatesPlugin');
export const [getXcyber360CorePlugin, setXcyber360CorePlugin] =
  createGetterSetter<Xcyber360CheckUpdatesPluginStart>('Xcyber360CorePlugin');
export const [getXcyber360EnginePlugin, setXcyber360EnginePlugin] =
  createGetterSetter<Xcyber360EnginePluginStart>('Xcyber360EnginePlugin');
export const [getHeaderActionMenuMounter, setHeaderActionMenuMounter] =
  createGetterSetter<AppMountParameters['setHeaderActionMenu']>(
    'headerActionMenuMounter',
  );
export const [getXcyber360FleetPlugin, setXcyber360FleetPlugin] =
  createGetterSetter<Xcyber360FleetPluginStart>('Xcyber360FleetPlugin');

/**
 * set bootstrapped inner angular module
 */
export function setAngularModule(module: any) {
  angularModule = module;
}

/**
 * get boostrapped inner angular module
 */
export function getAngularModule() {
  return angularModule;
}

/**
 * set bootstrapped inner dicover module
 */
export function setDiscoverModule(module: any) {
  discoverModule = module;
}

/**
 * get boostrapped inner dicover module
 */
export function getDiscoverModule() {
  return discoverModule;
}

export const [getCookies, setCookies] = createGetterSetter<any>('Cookies');
