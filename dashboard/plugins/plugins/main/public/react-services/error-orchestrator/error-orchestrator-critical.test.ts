/*
 * Xcyber360 app - Unit test for ErrorOrchestratorCritical.
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

import { ErrorOrchestrator, UIErrorLog } from './types';
import { ErrorOrchestratorCritical } from './error-orchestrator-critical';
import { WzMisc } from '../../factories/misc';
import NavigationService from '../navigation-service';

jest.mock('../navigation-service', () => {
  let url = '';
  return {
    getInstance() {
      return {
        navigate(str: string) {
          url = str;
        },
      };
    },
    _getURL() {
      return url;
    },
  };
});

NavigationService;
describe('Xcyber360 Error Orchestrator Critical', () => {
  describe('Given a valid options params ', () => {
    it('Should be called mockSetBlankScr and redirect to BlankScreen', () => {
      const options: UIErrorLog = {
        context: 'unitTest',
        level: 'ERROR',
        severity: 'UI',
        display: true,
        store: false,
        error: {
          error: 'error name test1',
          message: 'message test1',
          title: 'title jest testing1',
        },
      };

      const mockSetBlankScr = (WzMisc.prototype.setBlankScr = jest.fn());

      const errorOrchestratorCritical: ErrorOrchestrator =
        new ErrorOrchestratorCritical();
      errorOrchestratorCritical.loadErrorLog(options);

      expect(mockSetBlankScr).toBeCalledTimes(1);
      expect(NavigationService._getURL()).toEqual('/blank-screen');
    });
  });
});
