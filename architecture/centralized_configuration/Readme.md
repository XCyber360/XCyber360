

# Centralized Configuration
## Index
- [Centralized Configuration](#centralized-configuration)
  - [Index](#index)
  - [Purpose](#purpose)
  - [Sequence diagram](#sequence-diagram)

## Purpose

One of the key features of Xcyber360 as a EDR is the Centralized Configuration, allowing to deploy configurations, policies, rootcheck descriptions or any other file from Xcyber360 Manager to any Xcyber360 Agent based on their grouping configuration. This feature has multiples actors: Xcyber360 Cluster (Master and Worker nodes), with `xcyber360-remoted` as the main responsible from the managment side, and Xcyber360 Agent with `xcyber360-agentd` as resposible from the client side.


## Sequence diagram
Sequence diagram shows the basic flow of Centralized Configuration based on the configuration provided. There are mainly three stages:
1. Xcyber360 Manager Master Node (`xcyber360-remoted`) creates every `remoted.shared_reload` (internal) seconds the files that need to be synchronized with the agents.
2. Xcyber360 Cluster as a whole (via `xcyber360-clusterd`) continuously synchronize files between Xcyber360 Manager Master Node and Xcyber360 Manager Worker Nodes
3. Xcyber360 Agent `xcyber360-agentd` (via ) sends every `notify_time` (ossec.conf) their status, being `merged.mg` hash part of it. Xcyber360 Manager Worker Node (`xcyber360-remoted`) will check if agent's `merged.mg` is out-of-date, and in case this is true, the new `merged.mg` will be pushed to Xcyber360 Agent.