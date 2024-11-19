import { When } from 'cypress-cucumber-preprocessor/steps';
import { xpathElementIsVisible, forceClickElementByXpath, getSelector, forceClickElement, elementIsVisible} from '../../utils/driver';

import { BASIC_MODULES} from '../../utils/pages-constants';
import { XCYBER360_MENU_PAGE as pageName} from '../../utils/pages-constants';
const xcyber360MenuButton = getSelector('xcyber360MenuButton', pageName);
When('The user goes to {}', (moduleName) => {
  
  cy.wait(500);
  elementIsVisible(xcyber360MenuButton);
  cy.wait(500);
  forceClickElement(xcyber360MenuButton);
  xpathElementIsVisible(getSelector(moduleName, BASIC_MODULES));
  forceClickElementByXpath(getSelector(moduleName, BASIC_MODULES));
});
