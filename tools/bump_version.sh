#!/bin/bash

# Bump source version
# Copyright (C) 2015, Xcyber360 Inc.
# May 2, 2017

# Syntax:
# bump_version [ -v <version> ] [ -r <revision> ] [ -p <product_version> ] [ -d <Date to bump to> ]
# bump_version [ -d <Date to bump to> ]
# -d <Date> Format: YYYY-mm-dd. Default: today
# -r <revision> Specify the new revision number, this field does not impact over packages.
# Usage:
# If -v option is present, the script will add the provided version, revision, product version, and date information.
# If -v option is not present, the script will update the existing version, revision, product version or date information
# with the values provided for -r, -p, and -d options.
# Example:
# ./bump_version.sh -v v3.0.0-alpha1 -r 3457 -p 3.0.0.1 -d 2024-06-10
# ./bump_version.sh -d 2024-06-10


cd $(dirname $0)

VERSION_FILE="../src/VERSION"
REVISION_FILE="../src/REVISION"
DEFS_FILE="../src/headers/defs.h"
XCYBER360_SERVER="../src/init/xcyber360-server.sh"
XCYBER360_AGENT="../src/init/xcyber360-client.sh"
XCYBER360_LOCAL="../src/init/xcyber360-local.sh"
NSIS_FILE="../src/win32/xcyber360-installer.nsi"
MSI_FILE="../src/win32/xcyber360-installer.wxs"
FW_INIT="../framework/xcyber360/__init__.py"
CLUSTER_INIT="../framework/xcyber360/core/cluster/__init__.py"
API_SETUP="../api/core/setup.py"
API_SPEC="../api/core/api/spec/spec.yaml"
COMMS_API_SETUP="../api/comms/setup.py"
VERSION_DOCU="../src/Doxyfile"
WIN_RESOURCE="../src/win32/version.rc"

# Xcyber360 Packages
## Find files to bump .spec, changelog, copyright, .pkgproj
SPEC_FILES=$(find ../packages -name *.spec -type f)
CHANGELOG_FILES=$(find ../packages -name changelog -type f)
COPYRIGHT_FILES=$(find ../packages -name copyright -type f)
PKGPROJ_FILES=$(find ../packages -name *.pkgproj -type f)

help(){
    echo 'Usage:'
    echo -e "\tSyntax: $0 [-v  <version> ] [ -r <revision> ] [ -p <product_version> ] [ -d <Date to bump to> ]"
    echo -e "\tSyntax: $0 -d <Update release date> "
    echo -e "\t -d <Date>. Format: YYYY-mm-dd. Default: 'today'"
    echo
    echo "Note:"
    echo -e '\t- If -v option is present, the script will add the provided version, revision, product version, and date information.'
    echo -e '\t- If -v option is not present, the script will update the existing version, revision, product version or date information'
    echo -e '\t with the values provided for -r, -p, and -d options.'
    echo 'Example:'
    echo -e "\t $0 -v v3.0.0-alpha1 -r 3457 -p 3.0.0.1 -d 2024-06-10"
    echo -e "\t $0 -d 2024-06-10"
    echo
    exit 1
}

if [ $# -le 1 ]; then
    help
fi

while [ -n "$1" ]
do
    case $1 in
    "-p")
        if [[ $2 =~ ^[[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+$ ]]
        then
            product=$2
        else
            echo "Error: product does not match 'X.X.X.X'"
            exit 1
        fi

        shift 2
        ;;
    "-r")
        if [[ $2 =~ ^[[:digit:]]+$ ]]
        then
            revision=$2
        else
            echo "Error: revision is not numeric."
            exit 1
        fi

        shift 2
        ;;
    "-d")
        if [[ $2 =~ ^[0-9]{4}-((0[1-9])|(1[0-2]))-(([0-2][1-9])|([12]0)|(3[01]))$ ]]
        then
            bump_date=$2
        else
            echo "Error: Invalid date. Format expected 'YYYY-mm-dd'."
            exit 1
        fi

        shift 2
        ;;
    "-v")
        if [[ $2 =~ ^v[[:digit:]]+\.[[:digit:]]+\.[[:digit:]]+(-[[:alnum:]]+)?$ ]]
        then
            version=$2
        else
            echo "Error: incorrect version (must have form 'vX.X.X' or 'vX.X.X-...')."
            exit 1
        fi

        shift 2
        ;;
    *)
        help
    esac
done


if [ -n "$version" ]
then

    # File VERSIONS

    echo $version > $VERSION_FILE

    # File defs.h

    egrep "^#define __ossec_version +\"v.+\"" $DEFS_FILE > /dev/null

    if [ $? != 0 ]
    then
        echo "Error: no suitable version definition found at file $DEFS_FILE"
        exit 1
    fi

    sed -E -i'' -e "s/^(#define __ossec_version +)\"v.*\"/\1\"$version\"/" $DEFS_FILE

    # xcyber360-control

    sed -E -i'' -e "s/^(VERSION=+)\"v.*\"/\1\"$version\"/" $XCYBER360_SERVER
    sed -E -i'' -e "s/^(VERSION=+)\"v.*\"/\1\"$version\"/" $XCYBER360_AGENT
    sed -E -i'' -e "s/^(VERSION=+)\"v.*\"/\1\"$version\"/" $XCYBER360_LOCAL

    # File xcyber360-installer.nsi

    egrep "^\!define VERSION \".+\"" $NSIS_FILE > /dev/null

    if [ $? != 0 ]
    then
        echo "Error: no suitable version definition found at file $NSIS_FILE"
        exit 1
    fi

    sed -E -i'' -e "s/^(\!define VERSION \").+\"/\1${version:1}\"/g" $NSIS_FILE

    # File xcyber360-installer.wxs

    egrep '<Product Id="\*" Name="Xcyber360 Agent" Language="1033" Version=".+" Manufacturer=' $MSI_FILE > /dev/null

    if [ $? != 0 ]
    then
        echo "Error: no suitable version definition found at file $MSI_FILE"
        exit 1
    fi

    sed -E -i'' -e "s/(<Product Id=\"\*\" Name=\"Xcyber360 Agent\" Language=\"1033\" Version=\").+(\" Manufacturer=)/\1${version:1}\2/g" $MSI_FILE

    # Framework

    sed -E -i'' -e "s/__version__ = '.+'/__version__ = '${version:1}'/g" $FW_INIT

    # Cluster

    sed -E -i'' -e "s/__version__ = '.+'/__version__ = '${version:1}'/g" $CLUSTER_INIT

    # API

    sed -E -i'' -e "s/version='.+',/version='${version:1}',/g" $API_SETUP
    sed -E -i'' -e "s/version: '.+'/version: '${version:1}'/g" $API_SPEC
    sed -E -i'' -e "s_/v[0-9]+\.[0-9]+\.[0-9]+_/${version}_g" $API_SPEC
    sed -E -i'' -e "s_com/[0-9]+\.[0-9]+_com/$(expr match "$version" 'v\([0-9]*.[0-9]*\).*')_g" $API_SPEC

    # Communications API

    sed -E -i'' -e "s/version='.+',/version='${version:1}',/g" $COMMS_API_SETUP

    # Documentation config file

    sed -E -i'' -e "s/PROJECT_NUMBER         = \".+\"/PROJECT_NUMBER         = \"$version\"/g" $VERSION_DOCU

    # version.rc

    egrep "^#define VER_PRODUCTVERSION_STR v.+" $WIN_RESOURCE > /dev/null

    if [ $? != 0 ]
    then
        echo "Error: no suitable version definition (VER_PRODUCTVERSION_STR) found at file $WIN_RESOURCE"
        exit 1
    fi

    sed -E -i'' -e "s/^(#define VER_PRODUCTVERSION_STR +)v.+/\1$version/" $WIN_RESOURCE

    egrep "^#define VER_PRODUCTVERSION [[:digit:]]+,[[:digit:]]+,[[:digit:]]+,[[:digit:]]+" $WIN_RESOURCE > /dev/null

    if [ $? != 0 ]
    then
        echo "Error: no suitable version definition (VER_PRODUCTVERSION) found at file $WIN_RESOURCE"
        exit 1
    fi

    product_commas=`echo "${version:1}.0" | tr '.' ','`
    sed -E -i'' -e "s/^(#define VER_PRODUCTVERSION +).+/\1$product_commas/" $WIN_RESOURCE
fi

if [ -n "$revision" ]
then
    CURRENT_VERSION=$(cat $VERSION_FILE)

    # File REVISION

    echo $revision > $REVISION_FILE

    # xcyber360-control

    sed -E -i'' -e "s/^(REVISION=+)\".*\"/\1\"$revision\"/" $XCYBER360_SERVER
    sed -E -i'' -e "s/^(REVISION=+)\".*\"/\1\"$revision\"/" $XCYBER360_AGENT
    sed -E -i'' -e "s/^(REVISION=+)\".*\"/\1\"$revision\"/" $XCYBER360_LOCAL

    # File xcyber360-installer.nsi

    egrep "^\!define REVISION \".+\"" $NSIS_FILE > /dev/null

    if [ $? != 0 ]
    then
        echo "Error: no suitable revision definition found at file $NSIS_FILE"
        exit 1
    fi

    sed -E -i'' -e "s/^(\!define REVISION \").+\"/\1$revision\"/g" $NSIS_FILE

    # Cluster

    sed -E -i'' -e "s/__revision__ = '.+'/__revision__ = '$revision'/g" $CLUSTER_INIT

    # API

    sed -E -i'' -e "s/x-revision: .+'/x-revision: '$revision'/g" $API_SPEC

    # Documentation config file

    sed -E -i'' -e "s/PROJECT_NUMBER         = \".+\"/PROJECT_NUMBER         = \"$CURRENT_VERSION-$revision\"/g" $VERSION_DOCU
fi

if [ -n "$product" ]
then

    # File xcyber360-installer.nsi

    egrep "^VIProductVersion \".+\"" $NSIS_FILE > /dev/null

    if [ $? != 0 ]
    then
        echo "Error: no suitable product definition found at file $NSIS_FILE"
        exit 1
    fi

    sed -E -i'' -e "s/^(VIProductVersion \").+\"/\1$product\"/g" $NSIS_FILE
fi

# Xcyber360 Packages
if [ -z "$version" ]
then
    UPDATE_RELEASE_DATE="yes"
    version=$(cat $VERSION_FILE)
fi

VERSION=$(sed 's/v//' <<< $version)
mayor=${VERSION%%.*}
minor=$(cut -d"." -f1 <<< ${VERSION#*.})
patch=${VERSION##*.}

if [ -z "$bump_date" ]
then
    bump_date=$(LC_ALL=en_US.UTF-8 TZ="UTC" date +"%F")
    echo "Use default date: $bump_date"
fi

bump_date=$(LC_ALL=en_US.UTF-8 TZ="UTC" date -d "$bump_date" +"%a, %d %b %Y %H:%M:%S %z")

# SPECS files
spec_date=$(LC_ALL=en_US.UTF-8 TZ="UTC" date -d "$bump_date" +"%a %b %d %Y")
for spec_file in $SPEC_FILES; do
    echo "Updating the release date of $version in $spec_file"
    if [ -z "$UPDATE_RELEASE_DATE" ] ; then
        sed -E -i'' "/%changelog/a * $spec_date support <info@xcyber360.com> - ${VERSION}\n\
- More info: https://documentation.xcyber360.com/current/release-notes/release-$mayor-$minor-$patch.html" $spec_file
    else
       sed -E -i'' "/%changelog/{N;s/\n.*support/\n* $spec_date support/}" $spec_file
    fi
done

# Deb changelog files
for changelog_file in $CHANGELOG_FILES; do
    echo "Updating the release date of $version in $changelog_file"
    install_type=$(sed -E 's/.*xcyber360-(manager|agent).*/xcyber360-\1/' <<< $changelog_file)
    if [ -z "$UPDATE_RELEASE_DATE" ] ; then
        changelog_string="$install_type (${VERSION}-RELEASE) stable; urgency=low\n\n  * More info: https://documentation.xcyber360.com/current/release-notes/release-$mayor-$minor-$patch.html\
\n\n -- Xcyber360, Inc <info@xcyber360.com>  $bump_date\n"
        # Add new version to changelog
        sed -i'' "1i $changelog_string" $changelog_file
    else
       sed -E -i'' "/$install_type \(${VERSION}-RELEASE\) stable; urgency=low/{N;N;N;N; s/> .*/>  $bump_date/}" $changelog_file
    fi
done

## Deb copyright files
for copyright_file in $COPYRIGHT_FILES; do
    sed -E -i'' "s/(\sXcyber360, Inc <info@xcyber360.com> on).*/\1 $bump_date/" $copyright_file
done

# MacOS pkgproj files
for pkgproj_file in $PKGPROJ_FILES; do
    sed -E -i'' "s/(<string>)([0-9]+\.){2}[0-9]+-[0-9]+(<\/string>)/\1$VERSION-1\3/" $pkgproj_file
    sed -E -i'' "s/(<string>xcyber360-agent-)([0-9]+\.){2}[0-9]+-[0-9]+/\1$VERSION-1/" $pkgproj_file
done
