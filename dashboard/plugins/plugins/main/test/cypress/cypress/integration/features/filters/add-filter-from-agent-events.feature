Feature: Validate that the pinned filter label is displayed - from event page

  As a Xcyber360 user
  i want to set a new filter from the agent page
  in order to manage them
  Background:
    Given The xcyber360 admin user is logged
    And The user navigates to the agent page
    And The user navigates to the agent dashboard

  @filter @actions
  Scenario Outline: The user add and pin filter - Check across the modules - from event page - <Module Name>
    When The user navigates to agentModule <Module Name>
    And The user moves to events page
    And The user adds a new filter
    And The user pins a filter
    And The user navigates to the agent page
    And The user navigates to the agent dashboard
    And The user navigates to agentModule <Module Name>
    Then The user checks if the filter is displayed
    Examples:
      | Module Name          |
      | Security Events      |
      | Integrity Monitoring |
      | System Auditing      |
      | Mitre & Attack       |
      | NIST                 |
      | TSC                  |
      | Policy Monitoring    |
      | PCIDSS               |
