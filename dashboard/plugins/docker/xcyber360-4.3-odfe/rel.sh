#!/usr/bin/env bash

odfe_versions=(
	"1.13.2"
)

xcyber360_versions=(
	"4.3.0"
	"4.3.1"
	"4.3.2"
	"4.3.3"
	"4.3.4"
	"4.3.5"
	"4.3.6"
	"4.3.7"
	"4.3.8"
  "4.3.9"
  "4.3.10"
)

usage() {
	echo
	echo "$0 opendistro_version xcyber360_manager_version action [saml]"
	echo
	echo "where"
	echo "  opendistro_version is one of " ${odfe_versions[*]}
	echo "  xcyber360_manager_version if one of " ${xcyber360_versions[*]}
	echo "  action is one of up | down | stop"
	echo "optionally add 'saml' as the last parameter to deploy a saml enabled environment"
	exit -1
}

if [ $# -lt	3 ]
  then
  	echo "Incorrect number of arguments " $#
    usage
fi

if [[ ! " ${odfe_versions[*]} " =~ " ${1} " ]]
 then
 	echo "Version ${1} not found in ${odfe_versions[*]}"
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
export KIBANA_CONF=./config/kibana/kibana.yml
export COMPOSE_PROJECT_NAME=odfe-rel-${ES_VERSION//./}

profile="standard"
if [[ "$4" =~ "saml" ]]
then
	profile="saml"
	export KIBANA_CONF=./config/kibana/kibana_saml.yml
fi

case "$3" in
	up)
		docker compose --profile $profile -f rel.yml up -Vd
		if [[ "${profile}" =~ "saml" ]]
		then
			./enable_saml.sh ${COMPOSE_PROJECT_NAME}
		fi

		# This installs Xcyber360 and integrates with a default ODFE stack
		echo
		echo "Install Xcyber360 ${XCYBER360_VERSION} into ODFE ${ES_VERSION} manually with:"
		echo
		echo "1. Install the Xcyber360 app for Kibana"
		echo "docker exec -ti  ${COMPOSE_PROJECT_NAME}-kibana-1  /usr/share/kibana/bin/kibana-plugin install https://packages.xcyber360.com/4.x/ui/kibana/xcyber360_kibana-${XCYBER360_VERSION}_7.10.2-1.zip"
		echo
    echo "2. Restart Kibana"
		echo "docker restart ${COMPOSE_PROJECT_NAME}-kibana-1"
		echo
    echo "3. Configure Kibana"
		echo "docker cp ./config/kibana/xcyber360.yml ${COMPOSE_PROJECT_NAME}-kibana-1:/usr/share/kibana/data/xcyber360/config/"
    echo
    echo "4. Open Kibana in a browser:"
    echo "https://localhost:${KIBANA_PORT:-5601}"
    echo
    echo "5. (Optional) Enroll an agent (Ubuntu 20.04):"
    echo "docker run --name ${COMPOSE_PROJECT_NAME}-agent --network ${COMPOSE_PROJECT_NAME} --label com.docker.compose.project=${COMPOSE_PROJECT_NAME} -d ubuntu:20.04 bash -c '"
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
		docker compose --profile $profile -f rel.yml down -v --remove-orphans
		;;
	stop)
		docker compose --profile $profile -f rel.yml -p ${COMPOSE_PROJECT_NAME} stop
		;;
	*)
		usage
		;;
esac
