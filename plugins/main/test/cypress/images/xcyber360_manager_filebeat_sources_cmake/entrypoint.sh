#!/usr/bin/env bash

WITNESS_FILE_PATH=/tmp/xcyber360_configurated

NODE_IP="${NODE_IP:-$1}"
NODE_NAME="${NODE_NAME:-$2}"
NODE_TYPE="${NODE_TYPE:-$3}"
NODE_KEY="${NODE_KEY:-9d273b53510fef702b54a92e9cffc82e}"
CLUSTER_NAME="${CLUSTER_NAME:-xcyber360}"
CLUSTER_DISABLED="${CLUSTER_DISABLED:-no}"

if [ ! -f $WITNESS_FILE_PATH ]; then
    # Set right permissions for test_config data
    chown root:xcyber360_server /var/xcyber360_server/etc/xcyber360_server.conf
    chown root:xcyber360_server /var/xcyber360_server/etc/client.keys
    chown -R xcyber360_server:xcyber360_server /var/xcyber360_server/queue/agent-groups
    chown -R xcyber360_server:xcyber360_server /var/xcyber360_server/etc/shared
    chown root:xcyber360_server /var/xcyber360_server/etc/shared/ar.conf
    chown -R xcyber360_server:xcyber360_server /var/xcyber360_server/queue/agent-info

    # Modify xcyber360_server.conf
    sed -i "s:<key></key>:<key>$NODE_KEY</key>:g" /var/xcyber360_server/etc/xcyber360_server.conf
    sed -i "s:<node>NODE_IP</node>:<node>$NODE_IP</node>:g" /var/xcyber360_server/etc/xcyber360_server.conf
    sed -i "s:<name>xcyber360</name>:<name>$CLUSTER_NAME</name>:g" /var/xcyber360_server/etc/xcyber360_server.conf
    sed -i -e "/<cluster>/,/<\/cluster>/ s|<disabled>[a-z]\+</disabled>|<disabled>$CLUSTER_DISABLED</disabled>|g" /var/xcyber360_server/etc/xcyber360_server.conf
    sed -i "s:<node_name>node01</node_name>:<node_name>$NODE_NAME</node_name>:g" /var/xcyber360_server/etc/xcyber360_server.conf
    sed -i "s:<node_type>master</node_type>:<node_type>$NODE_TYPE</node_type>:g" /var/xcyber360_server/etc/xcyber360_server.conf

    # Create a witness file
    touch $WITNESS_FILE_PATH
fi

chown root: /etc/filebeat/filebeat.yml
chmod go-w /etc/filebeat/filebeat.yml

service filebeat start

sleep 1

service xcyber360-manager restart
/var/xcyber360_server/bin/xcyber360-apid restart

/usr/bin/supervisord
