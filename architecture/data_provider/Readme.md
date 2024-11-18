

# Xcyber360 module: Data Provider architecture
## Index
- [Xcyber360 module: Data Provider architecture](#xcyber360-module-data-provider-architecture)
  - [Index](#index)
  - [Purpose](#purpose)
  - [Sequence diagrams](#sequence-diagrams)


## Purpose
Everyone knows the importance of having detailed system information from our environment to take decisions based on specific use cases. Having detailed and valuable information about our environment helps us react to under unpredictable scenarios. Xcyber360 agents are able to collect interesting and valuable system information regarding processes, hardware, packages, OS, network and ports.

The System Inventory feature interacts with different modules to split responsibilities and optimize internal dependencies:
- Data Provider: Module in charge of gathering system information based on OSes. This involves information about current running processes, packages/programs installed, ports being used, network adapters and OS general information.
- DBSync: This module has one single main responsibility: Database management. It manages all database related operations like insertion, update, selection and deletion. This allows Xcyber360 to centralize and unify database management to make it more robust and to avoid possible misleading data.
- RSync: It is in charge of database synchronization between Xcyber360 agents DBs and Xcyber360  manager DBs (each agent DB). RSync implements a unified and generic communication algorithm used to maintain Xcyber360 agents and Xcyber360 manager datasets consistency.
- Syscollector: Module in charge of getting system information from Data Provider module and updating the local agent database (through dbsync module). Once this is done, the rsync module calculates the information to synchronize with the Xcyber360 manager.


## Sequence diagrams
The different sequence diagrams illustrate the data provider's workflow to obtain the information.

- 001-sequence-windows-store-packages-info: Explains how the data provider module obtains the packages information from the Windows Store.

