#!/bin/sh

# Xcyber360 Installer Functions
# Copyright (C) 2015, Xcyber360 Inc.
# November 18, 2016.
#
# This program is free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation.

# File dependencies:
# ./src/init/shared.sh
# ./src/init/template-select.sh

##########
# GenerateService() $1=template
##########
GenerateService()
{
    SERVICE_TEMPLATE=./src/init/templates/${1}
    sed "s|XCYBER360_HOME_TMP|${INSTALLDIR}|g" ${SERVICE_TEMPLATE}
}

InstallCommon()
{
  XCYBER360_GROUP='xcyber360'
  XCYBER360_USER='xcyber360'
  INSTALL="install"
  XCYBER360_CONTROL_SRC='./init/xcyber360-server.sh'

  ./init/adduser.sh ${XCYBER360_USER} ${XCYBER360_GROUP} ${INSTALLDIR}

  # Folder for the engine api socket
  ${INSTALL} -d -m 0750 -o root -g ${XCYBER360_GROUP} ${INSTALLDIR}run/xcyber360-engine
  # Folder for persistent databases (vulnerability scanner, ruleset, connector).
  ${INSTALL} -d -m 0660 -o root -g ${XCYBER360_GROUP} ${INSTALLDIR}var/lib/xcyber360-engine
  # Folder for persistent databases (vulnerability scanner).
  ${INSTALL} -d -m 0660 -o root -g ${XCYBER360_GROUP} ${INSTALLDIR}var/lib/xcyber360-engine/vd
  # Folder for persistent databases (ruleset).
  ${INSTALL} -d -m 0660 -o root -g ${XCYBER360_GROUP} ${INSTALLDIR}var/lib/xcyber360-engine/ruleset
  # Folder for persistent queues for the indexer connector.
  ${INSTALL} -d -m 0660 -o root -g ${XCYBER360_GROUP} ${INSTALLDIR}var/lib/xcyber360-engine/indexer-connector

}

InstallPython()
{
    PYTHON_VERSION='3.10.15'
    PYTHON_FILENAME='python.tar.gz'
    PYTHON_INSTALLDIR=${INSTALLDIR}usr/share/xcyber360-server/framework/python/
    PYTHON_FULL_PATH=${PYTHON_INSTALLDIR}$PYTHON_FILENAME

    echo "Download Python ${PYTHON_VERSION} file"
    mkdir -p ${PYTHON_INSTALLDIR}
    wget -O ${PYTHON_FULL_PATH} http://packages.xcyber360.com/deps/50/libraries/python/${PYTHON_VERSION}/${PYTHON_FILENAME}

    tar -xf $PYTHON_FULL_PATH -C ${PYTHON_INSTALLDIR} && rm -rf ${PYTHON_FULL_PATH}

    mkdir -p ${INSTALLDIR}usr/share/xcyber360-server/lib

    ${INSTALL} -m 0660 -o ${XCYBER360_USER} -g ${XCYBER360_GROUP} ${PYTHON_INSTALLDIR}lib/libxcyber360ext.so ${INSTALLDIR}usr/share/xcyber360-server/lib
    ${INSTALL} -m 0660 -o ${XCYBER360_USER} -g ${XCYBER360_GROUP} ${PYTHON_INSTALLDIR}lib/libpython3.10.so.1.0 ${INSTALLDIR}usr/share/xcyber360-server/lib

    chown -R ${XCYBER360_USER}:${XCYBER360_GROUP} ${PYTHON_INSTALLDIR}
}

InstallPythonDependencies()
{
    PYTHON_BIN_PATH=${INSTALLDIR}usr/share/xcyber360-server/framework/python/bin/python3

    echo "Installing Python dependecies"
    ${PYTHON_BIN_PATH} -m pip install -r ../framework/requirements.txt
}

InstallServer()
{
    PYTHON_BIN_PATH=${INSTALLDIR}usr/share/xcyber360-server/framework/python/bin/python3

    ${MAKEBIN} --quiet -C ../framework install INSTALLDIR=/usr/share/xcyber360-server
    ${PYTHON_BIN_PATH} -m pip install ../framework/

    ## Install Server management API
    ${MAKEBIN} --quiet -C ../api install INSTALLDIR=/usr/share/xcyber360-server
    ${PYTHON_BIN_PATH} -m pip install ../api/

    ## Install Communications API
    ${MAKEBIN} --quiet -C ../api/comms install INSTALLDIR=/usr/share/xcyber360-server
    ${PYTHON_BIN_PATH} -m pip install ../apis/

}

checkDownloadContent()
{
    VD_FILENAME='vd_1.0.0_vd_4.10.0.tar.xz'
    VD_FULL_PATH=${INSTALLDIR}tmp/xcyber360-server/${VD_FILENAME}

    if [ "X${DOWNLOAD_CONTENT}" = "Xy" ]; then
        echo "Download ${VD_FILENAME} file"
        mkdir -p ${INSTALLDIR}tmp/xcyber360-server
        wget -O ${VD_FULL_PATH} http://packages.xcyber360.com/deps/vulnerability_model_database/${VD_FILENAME}

        chmod 640 ${VD_FULL_PATH}
        chown ${XCYBER360_USER}:${XCYBER360_GROUP} ${VD_FULL_PATH}
    fi
}

installEngineStore()
{
    STORE_FILENAME='engine_store_0.0.2_5.0.0.tar.gz'
    STORE_FULL_PATH=${INSTALLDIR}tmp/xcyber360-server/${STORE_FILENAME}
    STORE_URL=https://packages.xcyber360.com/deps/engine_store_model_database/${STORE_FILENAME}
    DEST_FULL_PATH=${INSTALLDIR}var/lib/xcyber360-server

    echo "Download ${STORE_FILENAME} file"
    mkdir -p ${INSTALLDIR}tmp/xcyber360-server
    wget -O ${STORE_FULL_PATH} ${STORE_URL}

    chmod 640 ${STORE_FULL_PATH}
    chown ${XCYBER360_USER}:${XCYBER360_GROUP} ${STORE_FULL_PATH}

    tar -xzf ${STORE_FULL_PATH} -C ${DEST_FULL_PATH}
    chown -R ${XCYBER360_USER}:${XCYBER360_GROUP} ${DEST_FULL_PATH}/engine/store
    chown -R ${XCYBER360_USER}:${XCYBER360_GROUP} ${DEST_FULL_PATH}/engine/kvdb
    find ${DEST_FULL_PATH}/engine/store -type d -exec chmod 750 {} \; -o -type f -exec chmod 640 {} \;
    find ${DEST_FULL_PATH}/engine/kvdb -type d -exec chmod 750 {} \; -o -type f -exec chmod 640 {} \;
}

InstallEngine()
{
  # Check if the content needs to be downloaded.
  checkDownloadContent
  ${INSTALL} -m 0750 -o root -g ${XCYBER360_GROUP} engine/build/main ${INSTALLDIR}bin/xcyber360-engine

  # Folder for the engine socket.
  ${INSTALL} -d -m 0750 -o root -g ${XCYBER360_GROUP} ${INSTALLDIR}run/xcyber360-server/

  # Folder for persistent databases (vulnerability scanner, ruleset, connector).
  ${INSTALL} -d -m 0750 -o root -g ${XCYBER360_GROUP} ${INSTALLDIR}var/lib/xcyber360-server/
  ${INSTALL} -d -m 0750 -o root -g ${XCYBER360_GROUP} ${INSTALLDIR}var/lib/xcyber360-server/vd
  ${INSTALL} -d -m 0750 -o root -g ${XCYBER360_GROUP} ${INSTALLDIR}var/lib/xcyber360-server/engine
  ${INSTALL} -d -m 0755 -o root -g ${XCYBER360_GROUP} ${INSTALLDIR}var/log/xcyber360-server
  ${INSTALL} -d -m 0755 -o root -g ${XCYBER360_GROUP} ${INSTALLDIR}var/log/xcyber360-server/engine

  #${INSTALL} -d -m 0750 -o root -g ${XCYBER360_GROUP} engine/build/tzdb ${INSTALLDIR}var/lib/xcyber360-server/engine/tzdb
  cp -rp engine/build/tzdb ${INSTALLDIR}var/lib/xcyber360-server/engine/
  chown -R root:${XCYBER360_GROUP} ${INSTALLDIR}var/lib/xcyber360-server/engine/tzdb
  chmod 0750 ${INSTALLDIR}var/lib/xcyber360-server/engine/tzdb
  chmod 0640 ${INSTALLDIR}var/lib/xcyber360-server/engine/tzdb/*

  ${INSTALL} -d -m 0750 -o root -g ${XCYBER360_GROUP} ${INSTALLDIR}var/lib/xcyber360-server/indexer-connector

  # Download and extract the Engine store
  installEngineStore
}

InstallXcyber360()
{
  InstallCommon
  InstallEngine
  InstallPython
  InstallPythonDependencies
  InstallServer
}

BuildEngine()
{
  cd engine

  # Configure the engine
  cmake --preset=relwithdebinfo --no-warn-unused-cli
  # Compile only the engine
  cmake --build build --target main -j $(nproc)

  cd ..
}
