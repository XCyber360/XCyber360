import { Xcyber360Config } from '../../react-services';
import { getWzConfig } from './get-config';

export function wzConfig() {
  return getWzConfig(new Xcyber360Config());
}
