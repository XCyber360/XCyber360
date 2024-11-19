import { CoreStart } from 'opensearch-dashboards/public';
import { createGetterSetter } from '../../../src/plugins/opensearch_dashboards_utils/common';
import { Xcyber360CorePluginStart } from '../../xcyber360-core/public';
import { AppPluginStartDependencies } from './types';

export const [getPlugins, setPlugins] =
  createGetterSetter<AppPluginStartDependencies>('Plugins');
export const [getCore, setCore] = createGetterSetter<CoreStart>('Core');
export const [getXcyber360Core, setXcyber360Core] =
  createGetterSetter<Xcyber360CorePluginStart>('Xcyber360Core');
