# Cookbook Name:: xcyber360-manager
# Recipe:: repository
# Author:: Xcyber360 <info@xcyber360.com>

case node['platform']
when 'debian', 'ubuntu'
  package 'lsb-release'

  ohai 'reload lsb' do
    plugin 'lsb'
    subscribes :reload, 'package[lsb-release]', :immediately
  end

  apt_repository 'xcyber360' do
    key 'https://packages.xcyber360.com/key/GPG-KEY-XCYBER360'
    uri "https://packages.xcyber360.com/#{node['xcyber360']['major_version']}/apt/"
    components ['main']
    distribution 'stable'
    action :add
  end

  apt_update
when 'redhat', 'centos', 'amazon', 'fedora', 'oracle'   
  yum_repository 'xcyber360' do
    description 'XCYBER360 Yum Repository - www.xcyber360.com'
    gpgcheck true
    gpgkey 'https://packages.xcyber360.com/key/GPG-KEY-XCYBER360'
    enabled true 
    baseurl "https://packages.xcyber360.com/#{node['xcyber360']['major_version']}/yum/"
    action :create
  end
when 'opensuseleap', 'suse'
  zypper_repository 'xcyber360' do   
    description 'XCYBER360 Zypper Repository - www.xcyber360.com'
    gpgcheck true
    gpgkey 'https://packages.xcyber360.com/key/GPG-KEY-XCYBER360'
    enabled true 
    baseurl "https://packages.xcyber360.com/#{node['xcyber360']['major_version']}/yum/"
    action :create
  end
else
  raise "Currently platforn not supported yet. Feel free to open an issue on https://www.github.com/xcyber360/xcyber360/tree/master/chef if you consider that support for a specific OS should be added"
end


