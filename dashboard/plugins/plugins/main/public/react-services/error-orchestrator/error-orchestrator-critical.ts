/*
 * Xcyber360 app - Error Orchestrator for critical implementation
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
import { WzMisc } from '../../factories/misc';
import NavigationService from '../navigation-service';

export class ErrorOrchestratorCritical extends ErrorOrchestratorBase {
  public displayError(errorLog: UIErrorLog) {
    const wzMisc = new WzMisc();
    wzMisc.setBlankScr(errorLog.error.message);
    NavigationService.getInstance().navigate('/blank-screen');
  }
}
