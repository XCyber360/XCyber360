#!/bin/bash

# Xcyber360 package builder
# Copyright (C) 2015, Xcyber360 Inc.
#
# This program is a free software; you can redistribute it
# and/or modify it under the terms of the GNU General Public
# License (version 2) as published by the FSF - Free Software
# Foundation.
set -e

build_directories() {
  local build_folder=$1
  local xcyber360_dir="$2"
  local future="$3"

  mkdir -p "${build_folder}"
  xcyber360_version="$(cat xcyber360*/src/VERSION| cut -d 'v' -f 2)"

  if [[ "$future" == "yes" ]]; then
    xcyber360_version="$(future_version "$build_folder" "$xcyber360_dir" $xcyber360_version)"
    source_dir="${build_folder}/xcyber360-server-${xcyber360_version}"
  else
    package_name="xcyber360-server-${xcyber360_version}"
    source_dir="${build_folder}/${package_name}"
    cp -R $xcyber360_dir "$source_dir"
  fi
  echo "$source_dir"
}

# Function to handle future version
future_version() {
  local build_folder="$1"
  local xcyber360_dir="$2"
  local base_version="$3"

  specs_path="$(find $xcyber360_dir -name SPECS|grep $SYSTEM)"

  local major=$(echo "$base_version" | cut -dv -f2 | cut -d. -f1)
  local minor=$(echo "$base_version" | cut -d. -f2)
  local version="${major}.30.0"
  local old_name="xcyber360-server-${base_version}"
  local new_name=xcyber360-server-${version}

  local new_xcyber360_dir="${build_folder}/${new_name}"
  cp -R ${xcyber360_dir} "$new_xcyber360_dir"
  find "$new_xcyber360_dir" "${specs_path}" \( -name "*VERSION*" -o -name "*changelog*" \
        -o -name "*.spec" \) -exec sed -i "s/${base_version}/${version}/g" {} \;
  sed -i "s/\$(VERSION)/${major}.${minor}/g" "$new_xcyber360_dir/src/Makefile"
  sed -i "s/${base_version}/${version}/g" $new_xcyber360_dir/src/init/xcyber360-server.sh
  echo "$version"
}

# Function to generate checksum and move files
post_process() {
  local file_path="$1"
  local checksum_flag="$2"
  local source_flag="$3"

  if [[ "$checksum_flag" == "yes" ]]; then
    sha512sum "$file_path" > /var/local/checksum/$(basename "$file_path").sha512
  fi

  if [[ "$source_flag" == "yes" ]]; then
    mv "$file_path" /var/local/xcyber360
  fi
}

# Main script body

# Script parameters
export REVISION="$1"
export JOBS="$2"
debug="$3"
checksum="$4"
future="$5"
src="$6"

build_dir="/build_xcyber360"

source helper_function.sh

set -x

# Download source code if it is not shared from the local host
if [ ! -d "/xcyber360-local-src" ] ; then
    git clone --branch ${XCYBER360_BRANCH} --recurse-submodules https://github.com/xcyber360/xcyber360.git
    cd xcyber360
    git submodule update --init --recursive
    short_commit_hash=$(git rev-parse --short HEAD)
    cd ..
else
    short_commit_hash="$(cd /xcyber360-local-src && git config --global --add safe.directory /xcyber360-local-src && git rev-parse --short HEAD)"
fi

# Build directories
source_dir=$(build_directories "$build_dir/server" "xcyber360*" $future)

xcyber360_version="$(cat $source_dir/src/VERSION| cut -d 'v' -f 2)"
# TODO: Improve how we handle package_name
# Changing the "-" to "_" between target and version breaks the convention for RPM or DEB packages.
# For now, I added extra code that fixes it.
package_name="xcyber360-server-${xcyber360_version}"
specs_path="$(find $source_dir -name SPECS|grep $SYSTEM)"

setup_build "$source_dir" "$specs_path" "$build_dir" "$package_name" "$debug"

set_debug $debug $sources_dir

# Installing build dependencies
cd $sources_dir
build_deps
build_package $package_name $debug "$short_commit_hash" "$xcyber360_version"

# Post-processing
get_package_and_checksum $xcyber360_version $short_commit_hash $src
