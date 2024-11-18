# Cookbook Name:: xcyber360-manager
# Attributes:: cluster
# Author:: Xcyber360 <info@xcyber360.com

# Cluster settings
default['ossec']['conf']['cluster'] = {
    'name' => 'xcyber360',
    'node_name' => 'node01',
    'node_type' => 'master',
    'key' => '',
    'port' => 1516,
    'bind_addr' => '0.0.0.0',
    'nodes' => {
        'node' => "NODE_IP"
    },
    'hidden' => false,
    'disabled' => true
}
