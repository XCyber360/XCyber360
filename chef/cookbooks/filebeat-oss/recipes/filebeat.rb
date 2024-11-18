# Cookbook Name:: filebeat-oss
# Recipe:: filebeat-oss
# Author:: Xcyber360 <info@xcyber360.com>

# Install filebeat-oss pacakge

case node['platform']
when 'debian','ubuntu'
  apt_package 'filebeat' do
    version "#{node['elk']['patch_version']}"
  end
when 'redhat', 'centos', 'amazon', 'fedora', 'oracle'
  if node['platform_version'] >= '8' 
    dnf_package 'filebeat' do
      version "#{node['elk']['patch_version']}"
    end
  else  
    yum_package 'filebeat' do
      version "#{node['elk']['patch_version']}"
    end
  end
when 'opensuseleap', 'suse'
  zypper_package 'filebeat' do
    version "#{node['elk']['patch_version']}"
  end  
else
  raise "Currently platforn not supported yet. Feel free to open an issue on https://www.github.com/xcyber360/xcyber360/tree/master/chef if you consider that support for a specific OS should be added"
end

# Edit the file /etc/filebeat/filebeat.yml

template "#{node['filebeat']['config_path']}/filebeat.yml" do
  source 'filebeat.yml.erb'
  owner 'root'
  group 'root'
  mode '0640'
  variables ({
    hosts: node['filebeat']['yml']['output']['elasticsearch']['hosts']
  })
end

# Download the alerts template for Elasticsearch

remote_file "#{node['filebeat']['config_path']}/#{node['filebeat']['alerts_template']}" do
  source "https://raw.githubusercontent.com/xcyber360/xcyber360/#{node['xcyber360']['minor_version']}/extensions/elasticsearch/#{node['elk']['major_version']}/#{node['filebeat']['alerts_template']}"
  owner 'root'
  group 'root'
  mode '0644'
end

# Download the Xcyber360 module for Filebeat

execute 'Extract Xcyber360 module' do
  command "curl -s https://packages.xcyber360.com/#{node['xcyber360']['major_version']}/filebeat/#{node['filebeat']['xcyber360_module']} | tar -xvz -C #{node['filebeat']['xcyber360_module_path']}"
  action :run
end

# Configure Filebeat certificates

directory "#{node['filebeat']['certs_path']}" do
  action :create 
end

ruby_block 'Copy certificate files' do
  block do
    if Dir.exist?("#{node['elastic']['certs_path']}")
      IO.copy_stream("#{node['elastic']['certs_path']}/filebeat.pem", "#{node['filebeat']['certs_path']}/filebeat.pem")
      IO.copy_stream("#{node['elastic']['certs_path']}/filebeat.key", "#{node['filebeat']['certs_path']}/filebeat.key")
      IO.copy_stream("#{node['elastic']['certs_path']}/root-ca.pem", "#{node['filebeat']['certs_path']}/root-ca.pem")
    else 
      Chef::Log.fatal("Please copy the following files where Elasticserch is installed to 
        #{node['filebeat']['certs_path']}:
          - #{node['elastic']['certs_path']}/filebeat.pem
          - #{node['elastic']['certs_path']}/filebeat.key
          - #{node['elastic']['certs_path']}/root-ca.pem
        Then run as sudo:
          - systemctl daemon-reload
          - systemctl enable filebeat
          - systemctl start filebeat")
    end
  end
  action :run
end

# Enable and start service 

service "filebeat" do
  supports :start => true, :stop => true, :restart => true, :reload => true
  action [:enable, :start]
  only_if {
    File.exist?("#{node['filebeat']['certs_path']}/filebeat.pem") &&
    File.exist?("#{node['filebeat']['certs_path']}/filebeat.key") &&
    File.exist?("#{node['filebeat']['certs_path']}/root-ca.pem")
  }
end