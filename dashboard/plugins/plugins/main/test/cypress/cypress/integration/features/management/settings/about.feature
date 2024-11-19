Feature: Xcyber360 version information

  As a xcyber360 user
  I want to check the about information
  in order to see information about the system

  @about @actions
  Scenario: Check Xcyber360 version information
    Given The xcyber360 admin user is logged
    When The user navigates to About settings
    Then The Xcyber360 information is displayed
