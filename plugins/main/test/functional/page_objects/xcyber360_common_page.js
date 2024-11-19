/*
 * Xcyber360 app
 * Copyright (C) 2015-2022 Xcyber360, Inc.
 *
 * This program is free software; you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation; either version 2 of the License, or
 * (at your option) any later version.
 *
 * Find more information about this on the LICENSE file.
 */

export function Xcyber360CommonProvider({ getService, getPageObjects }) {
  const appsMenu = getService('appsMenu');
  const log = getService('log');
  const PageObjects = getPageObjects(['common', 'timePicker']);
  const testSubjects = getService('testSubjects');

  /**
   * Special functions needed in the tests.
   *
   * @class Xcyber360CommonPage
   */
  class Xcyber360CommonPage {
    /**
     * Navigate to `Security events` without the timestamp parameter in the URL
     *
     * @memberof Xcyber360CommonPage
     */
    async OpenSecurityEvents() {
      log.debug('Open Security events');
      await PageObjects.common.navigateToApp('settings');
      await appsMenu.clickLink('Xcyber360');
      await appsMenu.clickLink('Xcyber360');
      await testSubjects.click('overviewWelcomeGeneral');
    }

    /**
     * Navigate to `Integrity monitoring` without the timestamp parameter in the URL
     *
     * @memberof Xcyber360CommonPage
     */
    async OpenIntegrityMonitoring() {
      log.debug('Open Security events');
      await PageObjects.common.navigateToApp('settings');
      await appsMenu.clickLink('Xcyber360');
      await appsMenu.clickLink('Xcyber360');
      await testSubjects.click('overviewWelcomeFim');
    }

    /**
     * Select `today` in the commonly used times
     *
     * @memberof Xcyber360CommonPage
     */
    async setTodayRange() {
      log.debug('Set today in the time range picker');
      await PageObjects.timePicker.setCommonlyUsedTime(
        'superDatePickerCommonlyUsed_Today'
      );
      await PageObjects.common.sleep(3000);
      await testSubjects.click('querySubmitButton');
      await PageObjects.common.sleep(3000);
    }
  }
  return new Xcyber360CommonPage();
}
