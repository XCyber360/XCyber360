#!/bin/sh
# Copyright (C) 2015, Xcyber360 Inc.
# Created by Xcyber360, Inc. <info@xcyber360.com>.
# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

WPYTHON_BIN="framework/python/bin/python3"
XCYBER360_SHARE="/usr/share/xcyber360-server"

SCRIPT_PATH_NAME="$0"
SCRIPT_NAME="$(basename ${SCRIPT_PATH_NAME})"

PYTHON_SCRIPT="${XCYBER360_SHARE}/apis/scripts/$(echo ${SCRIPT_NAME} | sed 's/\-/_/g').py"

${XCYBER360_SHARE}/${WPYTHON_BIN} ${PYTHON_SCRIPT} $@
