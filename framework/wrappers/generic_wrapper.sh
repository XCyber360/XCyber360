#!/bin/sh


WPYTHON_BIN="framework/python/bin/python3"
XCYBER360_PATH="/usr/share/xcyber360-server"

SCRIPT_PATH_NAME="$0"
SCRIPT_NAME="$(basename ${SCRIPT_PATH_NAME})"

PYTHON_SCRIPT="${XCYBER360_PATH}/framework/scripts/$(echo ${SCRIPT_NAME} | sed 's/\-/_/g').py"

${XCYBER360_PATH}/${WPYTHON_BIN} ${PYTHON_SCRIPT} "$@"
