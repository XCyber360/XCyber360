# Cookbook Name:: xcyber360-manager
# Recipe:: manager
# Author:: Xcyber360 <info@xcyber360.com>

case node['platform']
when 'ubuntu', 'debian'
  apt_package 'xcyber360-manager' do
    version "#{node['xcyber360']['patch_version']}-1"
  end
when 'redhat', 'centos', 'amazon', 'fedora', 'oracle'
  if node['platform_version'] >= '8'
    dnf_package 'xcyber360-manager' do
      version "#{node['xcyber360']['patch_version']}-1"
    end
  else
    yum_package 'xcyber360-manager' do
      version "#{node['xcyber360']['patch_version']}-1"
    end
  end
when 'opensuseleap', 'suse'
  zypper_package 'xcyber360-manager' do
    version "#{node['xcyber360']['patch_version']}-1"
  end
else
  raise "Currently platforn not supported yet. Feel free to open an issue on https://www.github.com/xcyber360/xcyber360/tree/master/chef if you consider that support for a specific OS should be added"
end

# The dependences should be installed only when the cluster is enabled
if node['ossec']['conf']['cluster']['disabled'] == 'no'
  case node['platform']
  when 'ubuntu', 'debian'
    log 'Xcyber360_Cluster_not_compatible' do
      message "Xcyber360 cluster is not compatible with this version with #{node['platform']}"
      level :warn
    end
  when 'redhat', 'oracle', 'centos', 'amazon', 'fedora'
    if node['platform_version'].to_i == 7
      package ['python-setuptools', 'python-cryptography']
    end
  else
    raise "Currently platforn not supported yet. Feel free to open an issue on https://www.github.com/xcyber360/xcyber360/tree/master/chef if you consider that support for a specific OS should be added"
  end
end

# Auth need to be enable only in master node.
if node['ossec']['conf']['cluster']['node_type'] == 'master'
  execute 'Enable Authd' do
    command '/var/ossec/bin/xcyber360-control enable auth'
    not_if "ps axu | grep xcyber360-authd | grep -v grep"
  end
end

include_recipe 'xcyber360_manager::common'

template "#{node['ossec']['dir']}/etc/local_internal_options.conf" do
  source 'var/ossec/etc/manager_local_internal_options.conf'
  owner 'root'
  group 'ossec'
  mode '0640'
end

template "#{node['ossec']['dir']}/etc/rules/local_rules.xml" do
  source 'ossec_local_rules.xml.erb'
  owner 'root'
  group 'ossec'
  mode '0640'
end


template "#{node['ossec']['dir']}/etc/decoders/local_decoder.xml" do
  source 'ossec_local_decoder.xml.erb'
  owner 'root'
  group 'ossec'
  mode '0640'
end


template "#{node['ossec']['dir']}/api/configuration/api.yaml" do
  source 'api.yaml.erb'
  owner 'root'
  group 'ossec'
  mode '0660'
  variables(
    host: "#{node['api']['ip']}",
    port: "#{node['api']['port']}"
  )
end


service 'xcyber360' do
  service_name 'xcyber360-manager'
  supports :status => true, :restart => true, :reload => true
  action [:enable, :restart]
end
