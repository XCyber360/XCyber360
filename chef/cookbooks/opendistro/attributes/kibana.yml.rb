# frozen_string_literal: true

# Cookbook Name:: opendistro
# Attributes:: kibana.yml
# Author:: Xcyber360 <info@xcyber360.com>

# Kibana-oss configuration file

default['kibana']['yml'] = {
  'server' => {
    'host' => '0.0.0.0',
    'port' => 443
  },
  'elasticsearch' => {
    'hosts' => [
      "https://#{node['elastic']['yml']['network']['host']}:#{node['elastic']['yml']['http']['port']}"
    ]
  }
}