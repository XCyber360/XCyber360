# frozen_string_literal: true

# Cookbook Name:: elastic-stack
# Recipe:: kibana
# Author:: Xcyber360 <info@xcyber360.com>

# Install the Kibana package

case node['platform']
when 'debian', 'ubuntu'
  apt_package 'kibana' do
    version (node['elk']['patch_version']).to_s
  end
when 'redhat', 'centos', 'amazon', 'fedora', 'oracle'
  if node['platform_version'] >= '8'
    dnf_package 'kibana' do
      version (node['elk']['patch_version']).to_s
    end
  else
    yum_package 'kibana' do
      version (node['elk']['patch_version']).to_s
    end
  end
when 'opensuseleap', 'suse'
  zypper_package 'kibana' do
    version (node['elk']['patch_version']).to_s
  end
else
  raise 'Currently platforn not supported yet. Feel free to open an issue on https://www.github.com/xcyber360/xcyber360/tree/master/chef if you consider that support for a specific OS should be added'
end

# Create Kibana configuration file

template "#{node['kibana']['config_path']}/kibana.yml" do
  source 'kibana.yml.erb'
  owner 'kibana'
  group 'kibana'
  mode 0755
  variables({
              server_port: node['kibana']['yml']['server']['port'],
              server_host: node['kibana']['yml']['server']['host'],
              elasticsearch_hosts: node['kibana']['yml']['elasticsearch']['hosts']
            })
end

# Update the optimize and plugins directories permissions

execute "Change #{node['kibana']['package_path']}/optimize owner" do
  command "sudo chown -R kibana:kibana #{node['kibana']['package_path']}/optimize"
end

execute "Change #{node['kibana']['package_path']}/plugins owner" do
  command "sudo chown -R kibana:kibana #{node['kibana']['package_path']}/plugins"
end

# Install the Xcyber360 Kibana plugin

execute 'Create xcyber360.yml parent folders' do
  command "sudo -u kibana mkdir -p #{node['kibana']['package_path']}/optimize/xcyber360 && \
           sudo -u kibana mkdir -p #{node['kibana']['package_path']}/optimize/xcyber360/config"
end

execute 'Install the Xcyber360 app plugin for Kibana' do
  command "sudo -u kibana #{node['kibana']['package_path']}/bin/kibana-plugin install https://packages.xcyber360.com/#{node['xcyber360']['major_version']}/ui/kibana/xcyber360_kibana-#{node['xcyber360']['kibana_plugin_version']}-1.zip"
  not_if do
    File.exist?("#{node['kibana']['package_path']}/optimize/xcyber360/config/xcyber360.yml")
  end
end

# Configure Xcyber360-Kibana plugin configuration file

template "#{node['kibana']['package_path']}/optimize/xcyber360/config/xcyber360.yml" do
  source 'xcyber360.yml.erb'
  owner 'kibana'
  group 'kibana'
  mode 0755
  action :create
  variables({
              api_credentials: node['kibana']['xcyber360_api_credentials']
            })
end

# Enable and start the Kibana service

service 'kibana' do
  supports start: true, stop: true, restart: true, reload: true
  action %i[enable start]
end

# Wait for elastic and kibana services

ruby_block 'Wait for elasticsearch' do
  block do
    loop do
      break if begin
        TCPSocket.open(
          (node['elastic']['yml']['network']['host']).to_s,
          node['elastic']['yml']['http']['port']
        )
      rescue StandardError
        nil
      end

      puts 'Waiting elasticsearch....'; sleep 1
    end
  end
end

ruby_block 'Wait for kibana' do
  block do
    loop do
      break if begin
        TCPSocket.open(
          (node['kibana']['yml']['server']['host']).to_s,
          node['kibana']['yml']['server']['port']
        )
      rescue StandardError
        nil
      end
    end
  end
end

log 'Access Kibana web interface' do
  message "URL: http://#{node['kibana']['yml']['server']['host']}:#{node['kibana']['yml']['server']['port']}
  user: admin
  password: admin"
  level :info
end
