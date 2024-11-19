Feature: Read Kibana logs

  As a xcyber360 user
  I want to check the app logs
  in order to see information about the app logging

  @logs
  Scenario: Check Kibana logs
    Given The xcyber360 admin user is logged
    When The user navigates to Logs settings
    Then The Logs are displayed

  @logs
  Scenario: Reload Kibana logs
    Given The xcyber360 admin user is logged
    When The user navigates to Logs settings
    And The user reloads the logs
    Then The Logs are displayed
    And The backend response indicates that the logs are reloaded
