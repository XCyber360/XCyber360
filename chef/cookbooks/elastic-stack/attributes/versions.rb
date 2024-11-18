# frozen_string_literal: true

# Cookbook Name:: elastic-stack
# Attributes:: versions
# Author:: Xcyber360 <info@xcyber360.com>

# ELK
default['elk']['major_version'] = '7.x'
default['elk']['patch_version'] = '7.11.2'

# Xcyber360
default['xcyber360']['major_version'] = '4.x'
default['xcyber360']['minor_version'] = '4.4'
default['xcyber360']['patch_version'] = '4.4.0'

# Kibana
default['xcyber360']['kibana_plugin_version'] = '4.4.0_7.10.2'
