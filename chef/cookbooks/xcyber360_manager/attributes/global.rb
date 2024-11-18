# Cookbook Name:: xcyber360-manager
# Attributes:: global
# Author:: Xcyber360 <info@xcyber360.com

default['ossec']['conf']['global'] = {
    'jsonout_output' => true,
    'alerts_log' => true,
    'logall' => false,
    'logall_json' => false,
    'email_notification' => false,
    'smtp_server' => 'smtp.example.xcyber360.com',
    'email_from' => 'ossecm@example.xcyber360.com',
    'email_to' => 'recipient@example.xcyber360.com',
    'email_maxperhour' => 12,
    'email_log_source' => "alerts.log",
    'white_list' => [ 
        '127.0.0.1', 
        '^localhost.localdomain$', 
        '127.0.0.53'
    ]
}