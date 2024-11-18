# frozen_string_literal: true

# Cookbook Name:: elastic-stack
# Attributes:: api
# Author:: Xcyber360 <info@xcyber360.com>

default['kibana']['xcyber360_api_credentials'] = [
  {
    'id' => 'default',
    'url' => 'https://localhost',
    'port' => 55000,
    'username' => 'xcyber360',
    'password' => 'xcyber360',
  }
]
