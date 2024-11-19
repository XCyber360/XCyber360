#!/bin/bash
# Copyright (C) 2015, Xcyber360 Inc.

# validate OS, linux or macos
if [ "X$(uname)" = "XLinux" ] ; then
    # Get Xcyber360 installation path
    SCRIPT=$(readlink -f "$0")
    XCYBER360_HOME=$(dirname $(dirname $(dirname "$SCRIPT")))
    cd "${XCYBER360_HOME}"
    (sleep 5 && chmod +x ./var/upgrade/*.sh && ./var/upgrade/pkg_installer.sh && find ./var/upgrade/* -not -name upgrade_result -delete) >/dev/null 2>&1 &
else
    (sleep 5 && chmod +x ./var/upgrade/*.sh && ./var/upgrade/pkg_installer.sh && find ./var/upgrade/ -mindepth 1 -not -name upgrade_result -delete) >/dev/null 2>&1 &
fi