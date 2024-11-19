#!/bin/bash

PACKAGES_REPOSITORY=$1
DEBUG=$2

INSTALLER="/tmp/xcyber360-install.sh"
SYSTEM_USER="xcyber360-user"
HOSTNAME="xcyber360-server"
INDEXES=("xcyber360-alerts-*" "xcyber360-archives-*" "xcyber360-states-vulnerabilities-*" "xcyber360-statistics-*" "xcyber360-monitoring-*")

CURRENT_PATH="$( cd $(dirname $0) ; pwd -P )"
ASSETS_PATH="${CURRENT_PATH}/assets"
CUSTOM_PATH="${ASSETS_PATH}/custom"
INSTALL_ARGS="-a --install-dependencies"

if [[ "${PACKAGES_REPOSITORY}" == "dev" ]]; then
  INSTALL_ARGS+=" -d pre-release"
elif [[ "${PACKAGES_REPOSITORY}" == "staging" ]]; then
  INSTALL_ARGS+=" -d staging"
fi

if [[ "${DEBUG}" = "yes" ]]; then
  INSTALL_ARGS+=" -v"
fi

echo "Using ${PACKAGES_REPOSITORY} packages"

. ${ASSETS_PATH}/steps.sh

XCYBER360_VERSION=$(cat ${INSTALLER} | grep "xcyber360_version=" | cut -d "\"" -f 2)

# System configuration
echo "Configuring system"
systemConfig

# Edit installation script
echo "Editing installation script"
preInstall

# Install
echo "Installing Xcyber360 central components"
bash ${INSTALLER} ${INSTALL_ARGS}

echo "Stopping Filebeat and Xcyber360 Manager"
systemctl stop filebeat xcyber360-manager

# Delete indexes
echo "Deleting indexes"
for index in "${INDEXES[@]}"; do
    curl -u admin:admin -XDELETE "https://127.0.0.1:9200/$index" -k
done

# Recreate empty indexes (xcyber360-alerts and xcyber360-archives)
echo "Recreating empty indexes"
bash /usr/share/xcyber360-indexer/bin/indexer-security-init.sh -ho 127.0.0.1

echo "Stopping Xcyber360 indexer and Xcyber360 dashboard"
systemctl stop xcyber360-indexer xcyber360-dashboard
systemctl enable xcyber360-manager

echo "Cleaning system"
clean
