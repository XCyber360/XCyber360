/*
 * Xcyber360 app - Pattern Handler service
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

import store from '../redux/store';
import { updateAppConfig } from '../redux/actions/appConfigActions';

export class Xcyber360Config {
  constructor() {
    if (!!Xcyber360Config.instance) {
      return Xcyber360Config.instance;
    }
    Xcyber360Config.instance = this;

    return this;
  }

  /**
   * Set given configuration
   * @param {Object} cfg
   */
  setConfig(cfg) {
    store.dispatch(updateAppConfig({ ...cfg }));
  }

  /**
   * Get configuration
   */
  getConfig() {
    return store.getState().appConfig.data;
  }
}
