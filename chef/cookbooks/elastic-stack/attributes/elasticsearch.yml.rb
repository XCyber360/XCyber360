# frozen_string_literal: true

# Cookbook Name:: elastic-stack
# Attributes:: elasticsearch.yml
# Author:: Xcyber360 <info@xcyber360.com>

# Elasticsearch configuration file
default['elastic']['yml'] = {
  'cluster' => {
    'name' => 'es-xcyber360',
    'initial_master_nodes' => [
      'es-node-01'
    ]
  },
  'node' => {
    'name' => 'es-node-01'
  },
  'path' => {
    'data' => '/var/lib/elasticsearch',
    'logs' => '/var/log/elasticsearch'
  },
  'network' => {
    'host' => '0.0.0.0'
  },
  'http' => {
    'port' => 9200
  }
}
