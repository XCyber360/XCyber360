Feature: Should List Decoders And Show The Pager

  As a xcyber360 user
  i want to see the Decoders pages
  in order to manage them
  
  @decoder @actions
  Scenario: Should List Decoders And Show The Pager
    Given The xcyber360 admin user is logged
    When The user navigates to decoders
    Then The user should see the decoders
  
  @decoder @actions
  Scenario: Should List Custom Decoders And Show The Pager
    Given The xcyber360 admin user is logged
    When The user navigates to decoders
    When The user clicks the custom decoders button
    Then The user should see the decoders
  
  @decoder @actions
  Scenario: Should can edit a decoder
    Given The xcyber360 admin user is logged
    When The user navigates to decoders
    When The user clicks the custom decoders button
    When The user presses the edit decoders button and edits it
    Then The user should see the message
