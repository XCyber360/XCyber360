# frozen_string_literal: true

# Cookbook Name:: opendistro
# Recipe:: repository
# Author:: Xcyber360 <info@xcyber360.com>

case node['platform']
when 'debian', 'ubuntu'
  package 'lsb-release'

  ohai 'reload lsb' do
    plugin 'lsb'
    subscribes :reload, 'package[lsb-release]', :immediately
  end

  # Install GPG key and add repository
  apt_repository 'xcyber360' do
    uri "https://packages.xcyber360.com/#{node['xcyber360']['major_version']}/apt/"
    key 'https://packages.xcyber360.com/key/GPG-KEY-XCYBER360'
    distribution 'stable'
    components ['main']
  end

  # Update the package information
  apt_update
when 'redhat', 'centos', 'amazon', 'fedora', 'oracle'
  yum_repository 'xcyber360' do
    description 'Opendistroforelasticseach Yum'
    baseurl "https://packages.xcyber360.com/#{node['xcyber360']['major_version']}/yum/"
    gpgkey 'https://packages.xcyber360.com/key/GPG-KEY-XCYBER360'
    action :create
  end
when 'opensuseleap', 'suse'
  zypper_repository 'xcyber360' do
    description 'Opendistroforelasticseach Zypper'
    baseurl "https://packages.xcyber360.com/#{node['xcyber360']['major_version']}/yum/"
    gpgkey 'https://packages.xcyber360.com/key/GPG-KEY-XCYBER360'
    action :create
    not_if do
      File.exist?('/etc/zypp/repos.d/xcyber360.repo')
    end
  end
else
  raise 'Currently platforn not supported yet. Feel free to open an issue on https://www.github.com/xcyber360/xcyber360/tree/master/chef if you consider that support for a specific OS should be added'
end
