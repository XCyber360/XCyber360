import { WzMisc } from '../../factories/misc';
import { Xcyber360Config } from '../../react-services';
import { getWzConfig } from './get-config';
import { settingsWizard } from './settings-wizard';

export function nestedResolve(params) {
  const wzMisc = new WzMisc();
  const healthCheckStatus = sessionStorage.getItem('healthCheck');
  if (!healthCheckStatus) return;
  const xcyber360Config = new Xcyber360Config();
  return getWzConfig(xcyber360Config).then(() =>
    settingsWizard(
      params,
      wzMisc,
      params.location && params.location.pathname.includes('/health-check'),
    ),
  );
}
