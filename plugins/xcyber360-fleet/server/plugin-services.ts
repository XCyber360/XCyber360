import {
  CoreStart,
  ISavedObjectsRepository,
} from 'opensearch-dashboards/server';
import { createGetterSetter } from '../../../src/plugins/opensearch_dashboards_utils/common';
import { Xcyber360CorePluginStart } from '../../xcyber360-core/server';

export const [getInternalSavedObjectsClient, setInternalSavedObjectsClient] =
  createGetterSetter<ISavedObjectsRepository>('SavedObjectsRepository');
export const [getCore, setCore] = createGetterSetter<CoreStart>('Core');
export const [getXcyber360Core, setXcyber360Core] =
  createGetterSetter<Xcyber360CorePluginStart>('Xcyber360Core');
export const [getXcyber360FleetServices, setXcyber360FleetServices] =
  createGetterSetter<any>('Xcyber360FleetServices');
