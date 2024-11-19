import { When } from 'cypress-cucumber-preprocessor/steps';
import { clickElement, elementIsVisible, getSelector} from '../../utils/driver';

import { XCYBER360_MENU_PAGE as pageName} from '../../utils/pages-constants';
const xcyber360MenuButton = getSelector('xcyber360MenuButton', pageName);
const managementButton = getSelector('managementButton', pageName);
const reportingLink = getSelector('reportingLink', pageName);

When('The user navigates to management-reporting', () => {
  elementIsVisible(xcyber360MenuButton);
  clickElement(xcyber360MenuButton);
  cy.wait(500);
  elementIsVisible(managementButton);
  clickElement(managementButton);
  elementIsVisible(reportingLink);
  clickElement(reportingLink);
  });
