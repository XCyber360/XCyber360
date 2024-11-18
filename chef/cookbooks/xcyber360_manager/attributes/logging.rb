# Cookbook Name:: xcyber360-manager
# Attributes:: logging
# Author:: Xcyber360 <info@xcyber360.com

# Choose between plain or json format (or both) for internal logs
default['ossec']['conf']['logging'] = {
    'log_format' => 'plain'
}