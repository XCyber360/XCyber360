import { When } from 'cypress-cucumber-preprocessor/steps';
import { clickElement, elementIsVisible, getSelector } from '../../utils/driver';
import { XCYBER360_MENU_PAGE as pageName, SETTINGS_MENU_LINKS } from '../../utils/pages-constants';
const settingsButton = getSelector('settingsButton', pageName);
const xcyber360MenuButton = getSelector('xcyber360MenuButton', pageName);
const xcyber360MenuLeft = getSelector('xcyber360MenuLeft', pageName);
const xcyber360MenuRight = getSelector('xcyber360MenuRight', pageName);
const xcyber360MenuSettingRight = getSelector('xcyber360MenuSettingRight', pageName);

When('The user navigates to {} settings', (menuOption) => {
  elementIsVisible(xcyber360MenuButton);
  clickElement(xcyber360MenuButton);
  elementIsVisible(xcyber360MenuLeft);
  elementIsVisible(xcyber360MenuRight);
  elementIsVisible(settingsButton);
  clickElement(settingsButton);
  elementIsVisible(xcyber360MenuSettingRight);
  if (Cypress.env('type') == 'wzd') {
    cy.wait(1000);
    elementIsVisible(getSelector(menuOption, SETTINGS_MENU_LINKS)).click()
  } else {
    elementIsVisible(getSelector(menuOption, SETTINGS_MENU_LINKS));
    clickElement(getSelector(menuOption, SETTINGS_MENU_LINKS));
  };
});
