/*
 * Xcyber360 app - Error Orchestrator for UI implementation
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

import { ErrorOrchestratorBase } from './error-orchestrator-base';
import { UIErrorLog } from './types';
import { UI_LOGGER_LEVELS } from '../../../common/constants';
import loglevel from 'loglevel';

export class ErrorOrchestratorUI extends ErrorOrchestratorBase {
  public loadErrorLog(errorLog: UIErrorLog) {
    super.loadErrorLog({
      ...errorLog,
      display: errorLog.level === UI_LOGGER_LEVELS.ERROR || errorLog.display,
    });
  }

  public displayError(errorLog: UIErrorLog) {
    switch (errorLog.level) {
      case UI_LOGGER_LEVELS.INFO:
        loglevel.info('',errorLog.error.error,'\n',errorLog.error); // this code add a line break to the log message
        break;
      case UI_LOGGER_LEVELS.WARNING:
        loglevel.warn('',errorLog.error.error,'\n',errorLog.error); // this code add a line break to the log message
        break;
      case UI_LOGGER_LEVELS.ERROR:
        loglevel.error('',errorLog.error.error,'\n',errorLog.error); // this code add a line break to the log message
        break;
      default:
        console.log('No error level', errorLog.error.message, errorLog.error.error.error, errorLog.error);
    }
  }
}
