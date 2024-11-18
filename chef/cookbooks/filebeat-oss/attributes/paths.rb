# Cookbook Name:: filebeat-oss
# Attribute:: paths
# Author:: Xcyber360 <info@xcyber360.com>

default['filebeat']['config_path'] = '/etc/filebeat'
default['filebeat']['xcyber360_module_path'] = '/usr/share/filebeat/module'
default['filebeat']['certs_path'] = "#{node['filebeat']['config_path']}/certs"
default['elastic']['config_path'] = "/etc/elasticsearch"
default['elastic']['certs_path'] = "#{node['elastic']['config_path']}/certs"