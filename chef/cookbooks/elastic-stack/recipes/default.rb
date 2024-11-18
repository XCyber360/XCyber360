# frozen_string_literal: true

# Cookbook Name:: elastic-stack
# Recipe:: default
# Author:: Xcyber360 <info@xcyber360.com>

include_recipe 'elastic-stack::prerequisites'
include_recipe 'elastic-stack::repository'
include_recipe 'elastic-stack::elasticsearch'
include_recipe 'elastic-stack::kibana'
