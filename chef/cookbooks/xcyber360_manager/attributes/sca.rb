# Cookbook Name:: xcyber360-manager
# Attributes:: sca
# Author:: Xcyber360 <info@xcyber360.com

default['ossec']['conf']['sca'] = {
    'enabled' => true,
    'scan_on_start' => true,
    'interval' => "12h",
    'skip_nfs' => true
}