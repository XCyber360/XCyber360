#!/usr/bin/env bash

elastic_versions=(
	"7.14.2"
	"7.14.1"
	"7.14.0"
	"7.13.4"
	"7.13.3"
	"7.13.2"
	"7.13.1"
	"7.13.0"
	"7.12.1"
	"7.11.2"
	"7.10.2"
)

xcyber360_versions=(
	"4.2.7"
	"4.2.6"
	"4.2.5"
	"4.2.4"
	"4.2.3"
	"4.2.2"
	"4.2.1"
	"4.2.0"
)

usage() {
	echo
	echo "$0 elastic_version xcyber360_manager_version action "
	echo
	echo "where"
	echo "  elastic_version is one of " ${elastic_versions[*]}
	echo "  xcyber360_manager_version if one of " ${xcyber360_versions[*]}
	echo "  action is one of up | down | stop"
	exit -1
}

if [ $# -ne 3 ]
  then
  	echo "Incorrect number of arguments " $#
    usage
fi

if [[ ! " ${elastic_versions[*]} " =~ " ${1} " ]]
 then
 	echo "Version ${1} not found in ${elastic_versions[*]}"
 	exit -1
fi

if [[ ! " ${xcyber360_versions[*]} " =~ " ${2} " ]]
 then
 	echo "Version ${2} not found in ${xcyber360_versions[*]}"
 	exit -1
fi

export ES_VERSION=$1
export XCYBER360_VERSION=$2
export ELASTIC_PASSWORD=${PASSWORD:-SecretPassword}
export KIBANA_PASSWORD=${PASSWORD:-SecretPassword}
export CLUSTER_NAME=cluster
export LICENSE=basic # or trial
export KIBANA_PORT=${PORT:-5601}
export COMPOSE_PROJECT_NAME=es-rel-${ES_VERSION//./}

case "$3" in
	up)
		# recreate volumes
		docker compose -f rel.yml up -Vd

		# This installs Xcyber360 and integrates with a default Elastic stack
		# v=$( echo -n $ES_VERSION | sed 's/\.//g' )
		echo
		echo "Install Xcyber360 ${XCYBER360_VERSION} into Elastic ${ES_VERSION} manually with:"
		echo
		echo "1. Install the Xcyber360 app for Kibana"
		echo "docker exec -ti ${COMPOSE_PROJECT_NAME}-kibana-1 /usr/share/kibana/bin/kibana-plugin install https://packages.xcyber360.com/4.x/ui/kibana/xcyber360_kibana-${XCYBER360_VERSION}_${ES_VERSION}-1.zip"
		echo
    echo "2. Restart Kibana"
		echo "docker restart ${COMPOSE_PROJECT_NAME}-kibana-1"
		echo
    echo "3. Configure Kibana"
		echo "docker cp ./config/kibana/xcyber360.yml ${COMPOSE_PROJECT_NAME}-kibana-1:/usr/share/kibana/data/xcyber360/config/"
    echo
    echo "4. Open Kibana in a browser:"
    echo "http://localhost:${KIBANA_PORT}"
    echo
    echo "5. (Optional) Enroll an agent (Ubuntu 20.04):"
    echo "docker run --name ${COMPOSE_PROJECT_NAME}-xcyber360.agent --network ${COMPOSE_PROJECT_NAME} --label com.docker.compose.project=${COMPOSE_PROJECT_NAME} -d ubuntu:20.04 bash -c '"
    echo "  apt update -y"
    echo "  apt install -y curl lsb-release"
    echo "  curl -so \xcyber360-agent-${XCYBER360_VERSION}.deb \\"
    echo "    https://packages.xcyber360.com/4.x/apt/pool/main/w/xcyber360-agent/xcyber360-agent_${XCYBER360_VERSION}-1_amd64.deb \\"
    echo "    && XCYBER360_MANAGER='xcyber360.manager' XCYBER360_AGENT_GROUP='default' dpkg -i ./xcyber360-agent-${XCYBER360_VERSION}.deb"
    echo
    echo "  /etc/init.d/xcyber360-agent start"
    echo "  tail -f /var/ossec/logs/ossec.log"
    echo "'"
    echo
		;;
	down)
		# delete volumes
		docker compose -f rel.yml down -v --remove-orphans
		;;
	stop)
		docker compose -f rel.yml -p ${COMPOSE_PROJECT_NAME} stop
		;;
	*)
		usage
		;;
esac
