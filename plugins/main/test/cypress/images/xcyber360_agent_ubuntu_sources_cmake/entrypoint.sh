#!/bin/bash

# Register agent if client.keys is empty
if [ ! -s /var/xcyber360_server/etc/client.keys ]; then
  groups=${JOIN_GROUPS:-default}
  password=""
  if [ ! -z ${JOIN_PASSWORD} ]; then
    password="-P ${JOIN_PASSWORD}"
  fi
  manager=${JOIN_MANAGER}
  sed -i "s:MANAGER_IP:$JOIN_MANAGER:g" /var/xcyber360_server/etc/xcyber360_server.conf
  /var/xcyber360_server/bin/agent-auth -m $manager -G $groups $password
fi

# Start the agent
service xcyber360-agent start
status=$?
if [ $status -ne 0 ]; then
  echo "Failed to start agent: $status"
  exit $status
fi

echo "Background jobs running, listening for changes"

while sleep 60; do
  service xcyber360-agent status > /dev/null 2>&1
  status=$?
  if [ $status -ne 0 ]; then
    echo "Looks like the agent died."
    exit 1
  fi
done
