# Cookbook Name:: xcyber360-manager
# Attributes:: alerts
# Author:: Xcyber360 <info@xcyber360.com

default['ossec']['conf']['alerts'] = {
    'log_alert_level' => 3,
    'email_alert_level' => 12
}