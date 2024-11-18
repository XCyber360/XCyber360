# Filebeat cookbook

This cookbook installs and configures Filebeat on the specified node.

## Attributes

* `files.rb`: initialize needed file names to install Filebeat
* `paths.rb`: initialize some main paths
* `versions.rb`: initialize versions for Xcyber360 and ELK
* `filebeat.yml.rb`: customize YAML configuration file for Filebeat

## Usage

See `xcyber360-manager` cookbook documentation.

## Recipes

### default.rb

Declares all recipes in the cookbook and installs Filebeat.

#### repository.rb

Append to repository path the URL and GPG key of Filebeat

#### filebeat.rb

* Install the package Filebeats
* Create the configuration of */etc/filebeat/filebeat.yml* with defined attributes in the ```attributes``` folder
* Download the alerts template for Elasticsearch
* Download the Xcyber360 module for Filebeat

## References

Check [Filebeat installation documentation](https://documentation.xcyber360.com/current/learning-xcyber360/build-lab/install-xcyber360-manager.html#install-filebeat) for more detail