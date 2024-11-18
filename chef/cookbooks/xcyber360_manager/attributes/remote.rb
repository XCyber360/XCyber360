# Cookbook Name:: xcyber360-manager
# Attributes:: remote
# Author:: Xcyber360 <info@xcyber360.com

# Remoted settings
default['ossec']['conf']['remote'] = {
    'connection' => 'secure',
    'port' => "1514",
    'protocol' => "tcp",
    'queue_size' => "131072"
}