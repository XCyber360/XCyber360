#
# Cookbook Name:: ossec
# Recipe:: repository
#
# Copyright 2015, Opscode, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

if platform_family?('ubuntu', 'debian')
  package 'lsb-release'

  ohai 'reload lsb' do
    plugin 'lsb'
    subscribes :reload, 'package[lsb-release]', :immediately
  end

  apt_repository 'xcyber360' do
    uri "https://packages.xcyber360.com/#{node['xcyber360']['major_version']}/apt/"
    key 'https://packages.xcyber360.com/key/GPG-KEY-XCYBER360'
    components ['main']
    distribution 'stable'
  end

  apt_update
elsif platform_family?('rhel', 'redhat', 'centos', 'amazon')
  yum_repository 'xcyber360' do
    description 'XCYBER360 Yum Repository - www.xcyber360.com'
    gpgcheck true
    gpgkey 'https://packages.xcyber360.com/key/GPG-KEY-XCYBER360'
    enabled true 
    baseurl "https://packages.xcyber360.com/#{node['xcyber360']['major_version']}/yum/"
    action :create
  end
elsif
   zypper_repository 'xcyber360' do
    description 'XCYBER360 Yum Repository - www.xcyber360.com'
    gpgcheck true
    gpgkey 'https://packages.xcyber360.com/key/GPG-KEY-XCYBER360'
    enabled true 
    baseurl "https://packages.xcyber360.com/#{node['xcyber360']['major_version']}/yum/"
    action :create
  end
else
  raise "Currently platforn not supported yet. Feel free to open an issue on https://www.github.com/xcyber360/xcyber360/tree/master/chef if you consider that support for a specific OS should be added"
end
