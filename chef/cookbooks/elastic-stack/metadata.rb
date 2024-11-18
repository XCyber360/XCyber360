# frozen_string_literal: true

name 'elastic-stack'
maintainer 'Xcyber360'
maintainer_email 'info@xcyber360.com'
license 'All rights reserved'
description 'Install/Configures elastic-stack'
long_description IO.read(File.join(File.dirname(__FILE__), 'README.md'))
version '0.1.0'
chef_version '>= 15.0'

%w[redhat centos oracle].each do |el|
  supports el, '>= 6.0'
end
supports 'amazon', '>= 1.0'
supports 'fedora', '>= 22.0'
supports 'debian', '>= 7.0'
supports 'ubuntu', '>= 12.04'
supports 'suse', '>= 12.0'
supports 'opensuse', '>= 42.0'

issues_url 'https://github.com/xcyber360/xcyber360/issues' if respond_to?(:issues_url)
source_url 'https://github.com/xcyber360/xcyber360/tree/master/chef' if respond_to?(:source_url)