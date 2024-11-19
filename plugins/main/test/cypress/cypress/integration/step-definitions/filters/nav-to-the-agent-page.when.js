import { When } from 'cypress-cucumber-preprocessor/steps';
import { clickElement, elementIsVisible, getSelector} from '../../utils/driver';

import { XCYBER360_MENU_PAGE as pageName} from '../../utils/pages-constants';
const xcyber360MenuButton = getSelector('xcyber360MenuButton', pageName);
const agentsButton = getSelector('agentsButton', pageName);

When('The user navigates to the agent page', () => {
  clickElement(xcyber360MenuButton);
  elementIsVisible(agentsButton);
  clickElement(agentsButton);
});
