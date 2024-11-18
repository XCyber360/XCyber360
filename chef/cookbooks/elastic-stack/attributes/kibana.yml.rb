# frozen_string_literal: true

# Cookbook Name:: elastic-stack
# Attributes:: kibana.yml
# Author:: Xcyber360 <info@xcyber360.com>

# Kibana configuration file
default['kibana']['yml'] = {
  'server' => {
    'host' => '0.0.0.0',
    'port' => 5601
  },
  'elasticsearch' => {
    'hosts' => [
      "http://#{node['elastic']['yml']['network']['host']}:#{node['elastic']['yml']['http']['port']}"
    ]
  }
}
