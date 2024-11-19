XCYBER360_IMAGE_VERSION=5.0.0
XCYBER360_VERSION=$(echo $XCYBER360_IMAGE_VERSION | sed -e 's/\.//g')
XCYBER360_TAG_REVISION=1
XCYBER360_CURRENT_VERSION=$(curl --silent https://api.github.com/repos/xcyber360/xcyber360/releases/latest | grep '["]tag_name["]:' | sed -E 's/.*\"([^\"]+)\".*/\1/' | cut -c 2- | sed -e 's/\.//g')
IMAGE_VERSION=${XCYBER360_IMAGE_VERSION}

# Xcyber360 package generator
# Copyright (C) 2023, Xcyber360 Inc.
#
# This program is a free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation.

XCYBER360_IMAGE_VERSION="5.0.0"
XCYBER360_TAG_REVISION="1"
XCYBER360_DEV_STAGE=""
FILEBEAT_MODULE_VERSION="0.4"

# -----------------------------------------------------------------------------

trap ctrl_c INT

clean() {
    exit_code=$1

    exit ${exit_code}
}

ctrl_c() {
    clean 1
}

# -----------------------------------------------------------------------------


build() {

    XCYBER360_VERSION="$(echo $XCYBER360_IMAGE_VERSION | sed -e 's/\.//g')"
    FILEBEAT_TEMPLATE_BRANCH="${XCYBER360_IMAGE_VERSION}"
    XCYBER360_FILEBEAT_MODULE="xcyber360-filebeat-${FILEBEAT_MODULE_VERSION}.tar.gz"
    XCYBER360_UI_REVISION="${XCYBER360_TAG_REVISION}"

    if  [ "${XCYBER360_DEV_STAGE}" ];then
        FILEBEAT_TEMPLATE_BRANCH="v${FILEBEAT_TEMPLATE_BRANCH}-${XCYBER360_DEV_STAGE,,}"
        if ! curl --output /dev/null --silent --head --fail "https://github.com/xcyber360/xcyber360/tree/${FILEBEAT_TEMPLATE_BRANCH}"; then
            echo "The indicated branch does not exist in the xcyber360/xcyber360 repository: ${FILEBEAT_TEMPLATE_BRANCH}"
            clean 1
        fi
    else
        if curl --output /dev/null --silent --head --fail "https://github.com/xcyber360/xcyber360/tree/v${FILEBEAT_TEMPLATE_BRANCH}"; then
            FILEBEAT_TEMPLATE_BRANCH="v${FILEBEAT_TEMPLATE_BRANCH}"
        elif curl --output /dev/null --silent --head --fail "https://github.com/xcyber360/xcyber360/tree/${FILEBEAT_TEMPLATE_BRANCH}"; then
            FILEBEAT_TEMPLATE_BRANCH="${FILEBEAT_TEMPLATE_BRANCH}"
        else
            XCYBER360_MASTER_VERSION="$(curl -s https://raw.githubusercontent.com/xcyber360/xcyber360/master/src/VERSION | sed -e 's/v//g')"
            if [ "${FILEBEAT_TEMPLATE_BRANCH}" == "${XCYBER360_MASTER_VERSION}" ]; then
                FILEBEAT_TEMPLATE_BRANCH="master"
            else
                echo "The indicated branch does not exist in the xcyber360/xcyber360 repository: ${FILEBEAT_TEMPLATE_BRANCH}"
                clean 1
            fi
        fi
    fi

    echo XCYBER360_VERSION=$XCYBER360_IMAGE_VERSION > .env
    echo XCYBER360_IMAGE_VERSION=$XCYBER360_IMAGE_VERSION >> .env
    echo XCYBER360_TAG_REVISION=$XCYBER360_TAG_REVISION >> .env
    echo FILEBEAT_TEMPLATE_BRANCH=$FILEBEAT_TEMPLATE_BRANCH >> .env
    echo XCYBER360_FILEBEAT_MODULE=$XCYBER360_FILEBEAT_MODULE >> .env
    echo XCYBER360_UI_REVISION=$XCYBER360_UI_REVISION >> .env

    docker-compose -f build-docker-images/build-images.yml --env-file .env build --no-cache
    docker build -t xcyber360/xcyber360-cert-tool:$XCYBER360_IMAGE_VERSION build-docker-images/cert-tool-image/

    return 0
}

# -----------------------------------------------------------------------------

help() {
    echo
    echo "Usage: $0 [OPTIONS]"
    echo
    echo "    -d, --dev <ref>              [Optional] Set the development stage you want to build, example rc1 or beta1, not used by default."
    echo "    -f, --filebeat-module <ref>  [Optional] Set Filebeat module version. By default ${FILEBEAT_MODULE_VERSION}."
    echo "    -r, --revision <rev>         [Optional] Package revision. By default ${XCYBER360_TAG_REVISION}"
    echo "    -v, --version <ver>          [Optional] Set the Xcyber360 version should be builded. By default, ${XCYBER360_IMAGE_VERSION}."
    echo "    -h, --help                   Show this help."
    echo
    exit $1
}

# -----------------------------------------------------------------------------

main() {
    while [ -n "${1}" ]
    do
        case "${1}" in
        "-h"|"--help")
            help 0
            ;;
        "-d"|"--dev")
            if [ -n "${2}" ]; then
                XCYBER360_DEV_STAGE="${2}"
                shift 2
            else
                help 1
            fi
            ;;
        "-f"|"--filebeat-module")
            if [ -n "${2}" ]; then
                FILEBEAT_MODULE_VERSION="${2}"
                shift 2
            else
                help 1
            fi
            ;;
        "-r"|"--revision")
            if [ -n "${2}" ]; then
                XCYBER360_TAG_REVISION="${2}"
                shift 2
            else
                help 1
            fi
            ;;
        "-v"|"--version")
            if [ -n "$2" ]; then
                XCYBER360_IMAGE_VERSION="$2"
                shift 2
            else
                help 1
            fi
            ;;
        *)
            help 1
        esac
    done

    build || clean 1

    clean 0
}

main "$@"
