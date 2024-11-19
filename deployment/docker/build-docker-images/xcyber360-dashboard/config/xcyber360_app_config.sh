#!/bin/bash
# Xcyber360 Docker Copyright (C) 2017, Xcyber360 Inc. (License GPLv2)

xcyber360_url="${XCYBER360_API_URL:-https://xcyber360}"
xcyber360_port="${API_PORT:-55000}"
api_username="${API_USERNAME:-xcyber360-wui}"
api_password="${API_PASSWORD:-xcyber360-wui}"
api_run_as="${RUN_AS:-false}"

dashboard_config_file="/usr/share/xcyber360-dashboard/data/xcyber360/config/xcyber360.yml"

declare -A CONFIG_MAP=(
  [pattern]=$PATTERN
  [checks.pattern]=$CHECKS_PATTERN
  [checks.template]=$CHECKS_TEMPLATE
  [checks.api]=$CHECKS_API
  [checks.setup]=$CHECKS_SETUP
  [timeout]=$APP_TIMEOUT
  [api.selector]=$API_SELECTOR
  [ip.selector]=$IP_SELECTOR
  [ip.ignore]=$IP_IGNORE
  [xcyber360.monitoring.enabled]=$XCYBER360_MONITORING_ENABLED
  [xcyber360.monitoring.frequency]=$XCYBER360_MONITORING_FREQUENCY
  [xcyber360.monitoring.shards]=$XCYBER360_MONITORING_SHARDS
  [xcyber360.monitoring.replicas]=$XCYBER360_MONITORING_REPLICAS
)

for i in "${!CONFIG_MAP[@]}"
do
    if [ "${CONFIG_MAP[$i]}" != "" ]; then
        sed -i 's/.*#'"$i"'.*/'"$i"': '"${CONFIG_MAP[$i]}"'/' $dashboard_config_file
    fi
done


grep -q 1513629884013 $dashboard_config_file
_config_exists=$?

if [[ $_config_exists -ne 0 ]]; then
cat << EOF >> $dashboard_config_file
hosts:
  - 1513629884013:
      url: $xcyber360_url
      port: $xcyber360_port
      username: $api_username
      password: $api_password
      run_as: $api_run_as
EOF
else
  echo "Xcyber360 APP already configured"
fi

