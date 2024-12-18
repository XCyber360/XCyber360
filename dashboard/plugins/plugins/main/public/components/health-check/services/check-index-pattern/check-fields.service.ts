/*
 * Xcyber360 app - Check index pattern fields service
 *
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 *
 */

import { AppState, SavedObject } from '../../../../react-services';
import { getDataPlugin } from '../../../../kibana-services';
import { CheckLogger } from '../../types/check_logger';

export const checkFieldsService = async (
  appConfig,
  checkLogger: CheckLogger,
) => {
  const patternId = AppState.getCurrentPattern();
  checkLogger.info(`Index pattern id in cookie: [${patternId}]`);

  checkLogger.info(`Getting index pattern data [${patternId}]...`);
  const pattern = await getDataPlugin().indexPatterns.get(patternId);
  checkLogger.info(`Index pattern data found: [${pattern ? 'yes' : 'no'}]`);

  checkLogger.info(
    `Refreshing index pattern fields: title [${pattern.title}], id [${pattern.id}]...`,
  );
  try {
    await SavedObject.refreshIndexPattern(pattern);
    checkLogger.action(
      `Refreshed index pattern fields: title [${pattern.title}], id [${pattern.id}]`,
    );
  } catch (error) {
    if (error.message.includes('No indices match pattern')) {
      checkLogger.warning(
        `Index pattern fields for title [${pattern.title}], id [${pattern.id}] could not be refreshed due to: ${error.message}. This could be an indicator of some problem in the generation, not running server service or configuration to ingest of alerts data.`,
      );
    }
  }
};
