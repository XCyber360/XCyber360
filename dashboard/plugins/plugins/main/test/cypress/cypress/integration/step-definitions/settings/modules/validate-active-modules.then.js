import { clickElement, elementIsVisible, getSelector } from '../../../utils/driver';
import { XCYBER360_MENU_PAGE as pageName, MODULES_CARDS } from '../../../utils/pages-constants';
const modulesButton = getSelector('modulesButton', pageName);
const modulesDirectoryLink = getSelector('modulesDirectoryLink', pageName);
const xcyber360MenuButton = getSelector('xcyber360MenuButton', pageName);
const xcyber360MenuLeft = getSelector('xcyber360MenuLeft', pageName);
const xcyber360MenuRight = getSelector('xcyber360MenuRight', pageName);
const xcyber360MenuSettingRight = getSelector('xcyber360MenuSettingRight', pageName);

Then('The activated modules with {} are displayed on home page', (moduleName) => {
  elementIsVisible(xcyber360MenuButton);
  clickElement(xcyber360MenuButton);
  elementIsVisible(xcyber360MenuLeft);
  elementIsVisible(xcyber360MenuRight);
  elementIsVisible(modulesButton);
  clickElement(modulesButton);
  elementIsVisible(xcyber360MenuSettingRight);
  elementIsVisible(modulesDirectoryLink);
  clickElement(modulesDirectoryLink);
  elementIsVisible(getSelector(moduleName, MODULES_CARDS));
});
