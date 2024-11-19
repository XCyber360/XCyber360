import { When } from 'cypress-cucumber-preprocessor/steps';
import { clickElement, elementIsVisible, getSelector } from '../../../utils/driver';
import { XCYBER360_MENU_PAGE as pageName} from '../../../utils/pages-constants';
const groupsLink = getSelector('groupsLink', pageName);
const xcyber360MenuButton = getSelector('xcyber360MenuButton', pageName);
const managementButton = getSelector('managementButton', pageName);

When('The user navigates to groups page', () => {
  elementIsVisible(xcyber360MenuButton);
  clickElement(xcyber360MenuButton);
  elementIsVisible(managementButton);
  clickElement(managementButton);
  elementIsVisible(groupsLink);
  clickElement(groupsLink);
});
