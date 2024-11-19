#!/usr/bin/env bash

versions=(
	"4.4.0"
	"4.4.1"
	"4.4.2"
	"4.4.3"
	"4.4.4"
  "4.4.5"
	"4.5.0"
	"4.5.1"
  "4.5.2"
  "4.5.3"
  "4.6.0"
  "4.7.0"
  "4.8.0"
)

xcyber360_api_version=(
	"0"
	"1"
	"2"
)

usage() {
	echo
	echo "./pre.sh xcyber360_version xcyber360_api_version action "
	echo
	echo "where"
	echo "  xcyber360_version is one of "${versions[*]}
	echo "  xcyber360_api_version is the patch version of xcyber360 4.4, for example " ${xcyber360_api_version[*]}
	echo "  action is one of up | down | stop"
	echo
	echo "In a minor release, the API should not change the version here bumps the API"
	echo " string returned for testing. This script generates the file "
	echo
	echo "    config/imposter/api_info.json"
	echo
	echo "used by the mock server"
	exit -1
}

if [ $# -ne 3 ]; then
	echo "Incorrect number of arguments " $#
	usage
fi

if [[ ! " ${versions[*]} " =~ " ${1} " ]]; then
	echo "Version ${1} not found in ${versions[*]}"
	exit -1
fi

[ -n "$2" ] && [ "$2" -eq "$2" ] 2>/dev/null
if [ $? -ne 0 ]; then
	echo "$2 is not number"
	exit -1
fi

patch_version=$2
cat <<EOF >config/imposter/api_info.json
{
  "data": {
    "title": "Xcyber360 API REST",
    "api_version": "4.4.${patch_version}",
    "revision": 40316,
    "license_name": "GPL 2.0",
    "license_url": "https://github.com/xcyber360/xcyber360/blob/4.4/LICENSE",
    "hostname": "imposter",
    "timestamp": "2022-06-13T17:20:03Z"
  },
  "error": 0
}
EOF

export XCYBER360_STACK=${1}
export KIBANA_PORT=5601
export KIBANA_PASSWORD=${PASSWORD:-SecretPassword}
export COMPOSE_PROJECT_NAME=wz-pre-${XCYBER360_STACK//./}

case "$3" in
up)
	# recreate volumes
	docker compose -f pre.yml up -Vd

	# This installs Xcyber360 and integrates with a default Xcyber360 stack
	# v=$( echo -n $XCYBER360_STACK | sed 's/\.//g' )
	echo
	echo "Install the pre-release package manually with:"
	echo
	echo "1. Uninstall current version of the Xcyber360 app:"
	echo "docker exec -ti ${COMPOSE_PROJECT_NAME}-xcyber360.dashboard-1  /usr/share/xcyber360-dashboard/bin/opensearch-dashboards-plugin remove xcyber360"
	echo
	echo "2. Restart Xcyber360 Dashboard:"
	echo "docker restart ${COMPOSE_PROJECT_NAME}-xcyber360.dashboard-1"
	echo
	echo "3. Copy the pre-release package to the running Xcyber360 Dashboard container:"
	echo docker cp xcyber360-4.4.${patch_version}-1.zip ${COMPOSE_PROJECT_NAME}-xcyber360.dashboard-1:/tmp
	echo
	echo "4. Install the package we have just uploaded:"
	echo "docker exec -ti  ${COMPOSE_PROJECT_NAME}-xcyber360.dashboard-1  /usr/share/xcyber360-dashboard/bin/opensearch-dashboards-plugin install file:///tmp/xcyber360-4.4.${patch_version}-1.zip"
	echo
	echo "5. Restart the Xcyber360 Dashboard container:"
	echo "docker restart ${COMPOSE_PROJECT_NAME}-xcyber360.dashboard-1"
	echo
	echo "6. Upload the Xcyber360 app configuration:"
	echo "docker cp ./config/xcyber360_dashboard/xcyber360.yml ${COMPOSE_PROJECT_NAME}-xcyber360.dashboard-1:/usr/share/xcyber360-dashboard/data/xcyber360/config/"
	echo
	echo "7. Access the running instance in:"
	echo "https://localhost:${KIBANA_PORT}"
	echo
	;;
down)
	# delete volumes
	docker compose -f pre.yml down -v --remove-orphans
	;;
stop)
	docker compose -f rel.yml -p ${COMPOSE_PROJECT_NAME} stop
	;;
*)
	echo "Action must be either up or down"
	usage
	;;
esac
