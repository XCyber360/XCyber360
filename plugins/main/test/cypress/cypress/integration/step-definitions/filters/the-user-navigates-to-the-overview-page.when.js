import { When } from 'cypress-cucumber-preprocessor/steps';
import { clickElement, elementIsVisible, getSelector} from '../../utils/driver';
import { XCYBER360_MENU_PAGE as pageName} from '../../utils/pages-constants';
const xcyber360MenuButton = getSelector('xcyber360MenuButton', pageName);
const modulesDirectoryLink = getSelector('modulesDirectoryLink', pageName);
const modulesButton = getSelector('modulesButton', pageName);

When('The user navigates overview page', () => {
  elementIsVisible(xcyber360MenuButton);
  clickElement(xcyber360MenuButton);
  elementIsVisible(modulesButton);
  clickElement(modulesButton);
  elementIsVisible(modulesDirectoryLink);
  clickElement(modulesDirectoryLink);
});
