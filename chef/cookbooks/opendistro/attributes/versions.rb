# frozen_string_literal: true

# Cookbook Name:: opendistro
# Attributes:: versions
# Author:: Xcyber360 <info@xcyber360.com>

# Elastic Stack
default['elk']['patch_version'] = '7.10.2'

# Opendistro
default['odfe']['patch_version'] = '1.13.2'

# Xcyber360
default['xcyber360']['major_version'] = '4.x'
default['xcyber360']['minor_version'] = '4.4'
default['xcyber360']['patch_version'] = '4.4.0'

# Kibana
default['xcyber360']['kibana_plugin_version'] = '4.4.0_7.10.2'

# Search guard
default['searchguard']['version'] = '1.8'
