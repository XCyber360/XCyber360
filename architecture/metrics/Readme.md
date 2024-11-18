

# Metrics

## Index

- [Metrics](#metrics)
  - [Index](#index)
  - [Purpose](#purpose)
  - [Sequence diagram](#sequence-diagram)

## Purpose

Xcyber360 includes some metrics to understand the behavior of its components, which allow to investigate errors and detect problems with some configurations. This feature has multiple actors: `xcyber360-remoted` for agent interaction messages, `xcyber360-analysisd` for processed events.

## Sequence diagram

The sequence diagram shows the basic flow of metric counters. These are the main flows:

1. Messages received by `xcyber360-remoted` from agents.
2. Messages that `xcyber360-remoted` sends to agents.
3. Events received by `xcyber360-analysisd`.
4. Events processed by `xcyber360-analysisd`.
