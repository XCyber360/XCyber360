# frozen_string_literal: true

# Cookbook Name:: opendistro
# Attributes:: elasticsearch.yml
# Author:: Xcyber360 <info@xcyber360.com>

# Elasticsearch-oss configuration file

default['elastic']['yml'] = {
  'network' => {
    'host' => '0.0.0.0'
  },
  'http' => {
    'port' => 9200
  },
  'node' => {
    'name' => 'odfe-node-1'
  },
  'cluster' => {
    'initial_master_nodes' => [
      'odfe-node-1'
    ]
  }
}