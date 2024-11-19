#!/usr/bin/env bash

versions=(
	"4.6.0"
)

usage() {
	echo
	echo "$0 version action [saml]"
	echo
	echo "where version is one of ${versions[*]}"
	echo "action is one of up | down | stop"
	echo "saml to deploy a saml enabled environment"
	exit -1
}

if [ $# -lt 2 ]; then
	echo "Incorrect number of arguments " $#
	usage
fi

if [[ ! " ${versions[*]} " =~ " ${1} " ]]; then
	echo "Version ${1} not found in ${versions[*]}"
	exit -1
fi

export XCYBER360_STACK=${1}
export KIBANA_PORT=5601
export KIBANA_PASSWORD=${PASSWORD:-SecretPassword}
export COMPOSE_PROJECT_NAME=wz-rel-${XCYBER360_STACK//./}

profile="standard"
export XCYBER360_DASHBOARD_CONF=./config/xcyber360_dashboard/xcyber360_dashboard.yml
export SEC_CONFIG_FILE=./config/xcyber360_indexer/config.yml

if [[ "$3" =~ "saml" ]]; then
	profile="saml"
	export XCYBER360_DASHBOARD_CONF=./config/xcyber360_dashboard/xcyber360_dashboard_saml.yml
	export SEC_CONFIG_FILE=./config/xcyber360_indexer/config-saml.yml
fi

case "$2" in
up)
	docker compose --profile $profile -f rel.yml -p "${COMPOSE_PROJECT_NAME}" up -Vd
	echo
	echo "1. (Optional) Enroll an agent (Ubuntu 20.04):"
	echo "docker run --name ${COMPOSE_PROJECT_NAME}-agent --network ${COMPOSE_PROJECT_NAME} --label com.docker.compose.project=${COMPOSE_PROJECT_NAME} -d ubuntu:20.04 bash -c '"
	echo "  apt update -y"
	echo "  apt install -y curl lsb-release"
	echo "  curl -so \xcyber360-agent-${XCYBER360_STACK}.deb \\"
	echo "    https://packages.xcyber360.com/4.x/apt/pool/main/w/xcyber360-agent/xcyber360-agent_${XCYBER360_STACK}-1_amd64.deb \\"
	echo "    && XCYBER360_MANAGER='xcyber360.manager' XCYBER360_AGENT_GROUP='default' dpkg -i ./xcyber360-agent-${XCYBER360_STACK}.deb"
	echo
	echo "  /etc/init.d/xcyber360-agent start"
	echo "  tail -f /var/ossec/logs/ossec.log"
	echo "'"
	echo
	;;
down)
	docker compose --profile $profile -f rel.yml -p "${COMPOSE_PROJECT_NAME}" down -v --remove-orphans
	;;
stop)
	docker compose --profile $profile -f rel.yml -p "${COMPOSE_PROJECT_NAME}" stop
	;;
*)
	echo "Action must be either up or down"
	usage
	;;
esac
