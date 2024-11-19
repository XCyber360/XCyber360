import { When } from 'cypress-cucumber-preprocessor/steps';
import { clickElement, elementIsVisible, validateURLIncludes, getSelector } from '../../../utils/driver';
import { XCYBER360_MENU_PAGE as pageName} from '../../../utils/pages-constants';
const managementButton = getSelector('managementButton', pageName);
const xcyber360MenuButton = getSelector('xcyber360MenuButton', pageName);
const rulesLink = getSelector('rulesLink', pageName);

When('The user navigates to rules', () => {
  elementIsVisible(xcyber360MenuButton);
  clickElement(xcyber360MenuButton);
  elementIsVisible(managementButton);
  clickElement(managementButton);
  elementIsVisible(rulesLink);
  clickElement(rulesLink);
  validateURLIncludes('/manager/?tab=rules');
});
