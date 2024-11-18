# Xcyber360 indexer integration


|   |   |
|---|---|
| event.module | xcyber360-indexer |
| event.dataset | xcyber360-indexer-cluster, xcyber360-indexer-deprecation, xcyber360-indexer-slowlog, xcyber360-indexer-task |

Xcyber360 indexer module is designed to collect, parse, and analyze logs generated by [Xcyber360 indexer](https://documentation.xcyber360.com/current/getting-started/components/xcyber360-indexer.html).
The logs include valuable information for monitoring cluster operations and troubleshooting issues:
  - **Server logs:** These logs record events related to cluster configuration and status, such as changes in cluster topology, node startup or shutdown, shard allocation, etc.
  - **Slow logs:** These logs record operations that exceed certain predefined time thresholds, such as slow searches or slow indexings. Slow logs are useful for identifying and troubleshooting performance issues.
    - Search slow log
    - Indexing slow log
  - **Task logs:** Xcyber360 indexer can log CPU time and memory utilization for the top N memory-expensive search tasks when task resource consumers are enabled. By default, task resource consumers will log the top 10 search tasks at 60 second intervals.
  - **Deprecation logs:** Deprecation logs record when clients make deprecated API calls to your cluster. These logs can help you identify and fix issues prior to upgrading to a new major version.


## Compatibility

This integration has been tested with Xcyber360 Indexer logs from version 4.4.

## Configuration


This integration ingests logs from `/var/log/xcyber360-indexer` directory (the location of the files can be configured in the localfile configuration).

As mentioned above, we use the logcollector source localfile to ingest the logs from all the files.

Adding to the ossec.conf file in the monitored node the following blocks:
```xml
<localfile>
  <location>/var/log/xcyber360-indexer/xcyber360-cluster_server.json</location>
  <log_format>json</log_format>
</localfile>

<localfile>
  <location>/var/log/xcyber360-indexer/xcyber360-cluster_deprecation.json</location>
  <log_format>json</log_format>
</localfile>

<localfile>
  <location>/var/log/xcyber360-indexer/xcyber360-cluster_index_indexing_slowlog.json</location>
  <log_format>json</log_format>
</localfile>

<localfile>
  <location>/var/log/xcyber360-indexer/xcyber360-cluster_index_search_slowlog.json</location>
  <log_format>json</log_format>
</localfile>

<localfile>
  <location>/var/log/xcyber360-indexer/xcyber360-cluster_task_detailslog.log</location>
  <log_format>syslog</log_format>
</localfile>
```


## Schema

## Decoders

| Name | Description |
|---|---|
| decoder/xcyber360-indexer-slowlog/0 | Decoder for Xcyber360 indexer search and indexing slow logs |
| decoder/xcyber360-indexer-server/0 | Decoder for Xcyber360 indexer server logs |
| decoder/xcyber360-indexer-task-plain/0 | Decoder for Xcyber360 indexer task logs in plain text |
| decoder/xcyber360-indexer-deprecation/0 | Decoder for Xcyber360 indexer deprecation logs |
## Rules

| Name | Description |
|---|---|
## Outputs

| Name | Description |
|---|---|
## Filters

| Name | Description |
|---|---|
## Changelog

| Version | Description | Details |
|---|---|---|
| 0.0.1-dev | Created integration for Xcyber360 indexer | [#17873](https://github.com/xcyber360/xcyber360/pull/17873) |