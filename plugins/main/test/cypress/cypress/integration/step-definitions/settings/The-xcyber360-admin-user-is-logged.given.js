import { Given } from 'cypress-cucumber-preprocessor/steps';
import { navigate, elementIsVisible, getSelector, getCookiesFromBrowser } from '../../utils/driver';
import { XCYBER360_MENU_PAGE as pageName } from '../../utils/pages-constants';
const xcyber360MenuButton = getSelector('xcyber360MenuButton', pageName);
let urlsList = [
  'https://localhost:5601/elastic/samplealerts/security',
  'https://localhost:5601/elastic/samplealerts/auditing-policy-monitoring',
  'https://localhost:5601/elastic/samplealerts/threat-detection',
];
let urlBodys = [
  { alertCount: 27000, index: 'xcyber360-alerts-4.x-sample-security' },
  { alertCount: 12000, index: 'xcyber360-alerts-4.x-sample-auditing-policy-monitoring' },
  { alertCount: 15000, index: 'xcyber360-alerts-4.x-sample-threat-detection' },
];

Given('The admin user is logged', () => {
  if (Cypress.env('type') != 'wzd') {
    navigate('app/xcyber360');
  } else {
    navigate('/');
  }
  elementIsVisible(xcyber360MenuButton);
});

Given('The sample data is loaded', () => {
  cy.readFile('cookies.json').then((cookies) => {
    let headersFormat = {
      'content-type': 'application/json; charset=utf-8',
      Cookie: getCookiesFromBrowser(cookies),
      Accept: 'application/json, text/plain, */*',
      'Accept-Encoding': 'gzip, deflate, br',
    };
    Cypress.env('type') == 'xpack'
      ? (headersFormat['kbn-xsrf'] = 'kibana')
      : (headersFormat['osd-xsrf'] = 'kibana');
    for (let i = 0; i < urlsList.length; i++) {
      cy.request({
        method: 'POST',
        url: urlsList[i],
        headers: headersFormat,
        body: urlBodys[i],
      }).should((response) => {
        expect(response.status).to.eq(200);
      });
    }
  });
});
