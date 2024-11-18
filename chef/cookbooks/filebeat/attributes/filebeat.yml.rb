# Cookbook Name:: filebeat
# Attribute:: filebeat.yml
# Author:: Xcyber360 <info@xcyber360.com>

default['filebeat']['yml'] = {
    'output' => {
        'elasticsearch' => {
            'hosts' => [
                {
                    'ip' => '0.0.0.0',
                    'port' => 9200
                }
            ]
        }
    }
}

