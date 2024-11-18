# frozen_string_literal: true

# Cookbook Name:: opendistro
# Attributes:: searchguard.yml
# Author:: Xcyber360 <info@xcyber360.com>

# Searchguard configuraion file

default['search_guard']['yml'] = {
  'nodes' => {
    'elasticsearch' => {
      'ip' => [
        (node['elastic']['yml']['network']['host']).to_s
      ]
    },
    'kibana' => {
      'ip' => [
        (node['kibana']['yml']['server']['host']).to_s
      ]
    }
  }
}