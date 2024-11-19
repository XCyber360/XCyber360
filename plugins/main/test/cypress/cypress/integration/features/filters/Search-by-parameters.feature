Feature: Search by parameters

    As a Xcyber360 user
    I want to pin a filter
    in order to aplly it across the modules
    Background:
        Given The xcyber360 admin user is logged
        And The sample data is loaded

    Scenario Outline: Search by parameters with AND
        When The user goes to <Module Name>
        And The user types a particular search <key> on the search bar
        Then The query is accepted and the results should be displayed
        Examples:
            | Module Name          | key                                              |
            | Security Events      | cluster.name : "xcyber360" and rule.level : "3"      |
            | Integrity Monitoring | cluster.name : "xcyber360" and agent.id : "001"      |
            | NIST                 | cluster.name : "xcyber360" and agent.name : "Ubuntu" |
            | TSC                  | cluster.name : "xcyber360" and agent.name : "Ubuntu" |
            | PCIDSS               | cluster.name : "xcyber360" and agent.name : "Ubuntu" |

    Scenario Outline: Search by parameters with OR
        When The user goes to <Module Name>
        And The user types a particular search <key> on the search bar
        Then The query is accepted and the results should be displayed
        Examples:
            | Module Name          | key                                             |
            | Security Events      | cluster.name : "xcyber360" or rule.level : "3"      |
            | Integrity Monitoring | cluster.name : "xcyber360" or agent.id : "001"      |
            | NIST                 | cluster.name : "xcyber360" or agent.name : "Ubuntu" |
            | TSC                  | cluster.name : "xcyber360" or agent.name : "Ubuntu" |
            | PCIDSS               | cluster.name : "xcyber360" or agent.name : "Ubuntu" |