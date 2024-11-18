%if %{_isstage} == no
  %define _rpmfilename %%{NAME}_%%{VERSION}-%%{RELEASE}_%%{ARCH}_%{_hashcommit}.rpm
%else
  %define _rpmfilename %%{NAME}-%%{VERSION}-%%{RELEASE}.%%{ARCH}.rpm
%endif

Summary:     Xcyber360 helps you to gain security visibility into your infrastructure by monitoring hosts at an operating system and application level. It provides the following capabilities: log analysis, file integrity monitoring, intrusions detection and policy and compliance monitoring
Name:        xcyber360-server
Version:     %{_version}
Release:     %{_release}
License:     GPL
Group:       System Environment/Daemons
Source0:     %{name}-%{version}.tar.gz
URL:         https://www.xcyber360.com/
BuildRoot:   %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Vendor:      Xcyber360, Inc <info@xcyber360.com>
Packager:    Xcyber360, Inc <info@xcyber360.com>
Requires(pre):    /usr/sbin/groupadd /usr/sbin/useradd
Requires(postun): /usr/sbin/groupdel /usr/sbin/userdel
AutoReqProv: no

Requires: coreutils
BuildRequires: coreutils glibc-devel automake autoconf libtool policycoreutils-python curl perl

ExclusiveOS: linux

%define _source_payload w9.xzdio
%define _binary_payload w9.xzdio

%description
Xcyber360 helps you to gain security visibility into your infrastructure by monitoring
hosts at an operating system and application level. It provides the following capabilities:
log analysis, file integrity monitoring, intrusions detection and policy and compliance monitoring

# Don't generate build_id links to prevent conflicts with other
# packages.
%global _build_id_links none

# Build debuginfo package
%debug_package
%package xcyber360-server-debuginfo
Summary: Debug information for package %{name}.
%description xcyber360-server-debuginfo
This package provides debug information for package %{name}.

%prep
%setup -q
%build
%install
# Clean BUILDROOT
rm -fr %{buildroot}
echo 'VCPKG_ROOT="/root/vcpkg"' > ./etc/preloaded-vars.conf
echo 'USER_LANGUAGE="en"' > ./etc/preloaded-vars.conf
echo 'USER_NO_STOP="y"' >> ./etc/preloaded-vars.conf
echo 'USER_INSTALL_TYPE="server"' >> ./etc/preloaded-vars.conf
echo 'USER_DIR="%{_localstatedir}"' >> ./etc/preloaded-vars.conf
echo 'USER_DELETE_DIR="y"' >> ./etc/preloaded-vars.conf
echo 'USER_UPDATE="n"' >> ./etc/preloaded-vars.conf
echo 'USER_ENABLE_EMAIL="n"' >> ./etc/preloaded-vars.conf
echo 'USER_WHITE_LIST="n"' >> ./etc/preloaded-vars.conf
echo 'USER_ENABLE_SYSLOG="y"' >> ./etc/preloaded-vars.conf
echo 'USER_ENABLE_AUTHD="y"' >> ./etc/preloaded-vars.conf
echo 'USER_SERVER_IP="MANAGER_IP"' >> ./etc/preloaded-vars.conf
echo 'USER_CA_STORE="/path/to/my_cert.pem"' >> ./etc/preloaded-vars.conf
echo 'USER_GENERATE_AUTHD_CERT="y"' >> ./etc/preloaded-vars.conf
echo 'USER_AUTO_START="n"' >> ./etc/preloaded-vars.conf
echo 'USER_CREATE_SSL_CERT="n"' >> ./etc/preloaded-vars.conf
echo 'DOWNLOAD_CONTENT="y"' >> ./etc/preloaded-vars.conf
export VCPKG_ROOT="/root/vcpkg"
export PATH="${PATH}:${VCPKG_ROOT}"
scl enable devtoolset-11 ./install.sh

# Create directories
mkdir -p ${RPM_BUILD_ROOT}%{_initrddir}

# Copy the installed files into RPM_BUILD_ROOT directory
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}tmp/
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}run/xcyber360-server
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}var/lib/xcyber360-server
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}usr/bin
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}var/log
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}usr/share/xcyber360-server
mkdir -p ${RPM_BUILD_ROOT}%{_localstatedir}etc/xcyber360-server

cp -p %{_localstatedir}usr/bin/xcyber360-engine ${RPM_BUILD_ROOT}%{_localstatedir}usr/bin/
cp -p %{_localstatedir}usr/bin/xcyber360-apid ${RPM_BUILD_ROOT}%{_localstatedir}usr/bin/
cp -p %{_localstatedir}usr/bin/xcyber360-comms-apid ${RPM_BUILD_ROOT}%{_localstatedir}usr/bin/
cp -p %{_localstatedir}usr/bin/xcyber360-server ${RPM_BUILD_ROOT}%{_localstatedir}usr/bin/

cp -pr %{_localstatedir}tmp/xcyber360-server ${RPM_BUILD_ROOT}%{_localstatedir}tmp/
cp -pr %{_localstatedir}run/xcyber360-server ${RPM_BUILD_ROOT}%{_localstatedir}run/
cp -pr %{_localstatedir}var/lib/xcyber360-server ${RPM_BUILD_ROOT}%{_localstatedir}var/lib/
cp -pr %{_localstatedir}var/log/xcyber360-server ${RPM_BUILD_ROOT}%{_localstatedir}var/log/
cp -pr %{_localstatedir}usr/share/xcyber360-server ${RPM_BUILD_ROOT}%{_localstatedir}usr/share/
cp -pr %{_localstatedir}etc/xcyber360-server ${RPM_BUILD_ROOT}%{_localstatedir}etc/

sed -i "s:XCYBER360_HOME_TMP:%{_localstatedir}:g" src/init/templates/xcyber360-server-rh.init
install -m 0755 src/init/templates/xcyber360-server-rh.init ${RPM_BUILD_ROOT}%{_initrddir}/xcyber360-server

mkdir -p ${RPM_BUILD_ROOT}/usr/lib/systemd/system/
sed -i "s:XCYBER360_HOME_TMP:%{_localstatedir}:g" src/init/templates/xcyber360-server.service
install -m 0644 src/init/templates/xcyber360-server.service ${RPM_BUILD_ROOT}/usr/lib/systemd/system/

%{_rpmconfigdir}/find-debuginfo.sh

%pre

# Create the xcyber360 group if it doesn't exists
if command -v getent > /dev/null 2>&1 && ! getent group xcyber360 > /dev/null 2>&1; then
  groupadd -r xcyber360
elif ! getent group xcyber360 > /dev/null 2>&1; then
  groupadd -r xcyber360
fi

# Create the xcyber360 user if it doesn't exists
if ! getent passwd xcyber360 > /dev/null 2>&1; then
  useradd -g xcyber360 -G xcyber360 -d %{_localstatedir} -r -s /sbin/nologin xcyber360
fi

# Stop the services to upgrade the package
if [ $1 = 2 ]; then
  if command -v systemctl > /dev/null 2>&1 && systemctl > /dev/null 2>&1 && systemctl is-active --quiet xcyber360-server > /dev/null 2>&1; then
    systemctl stop xcyber360-server.service > /dev/null 2>&1
    touch %{_localstatedir}/tmp/xcyber360.restart
  # Check for SysV
  elif command -v service > /dev/null 2>&1 && service xcyber360-server status 2>/dev/null | grep "is running" > /dev/null 2>&1; then
    service xcyber360-server stop > /dev/null 2>&1
    touch %{_localstatedir}/tmp/xcyber360.restart
  else
    echo "Unable to stop xcyber360-server. Neither systemctl nor service are available."
  fi
fi

%post

%define _vdfilename vd_1.0.0_vd_4.10.0.tar.xz

if [[ -d /run/systemd/system ]]; then
  rm -f %{_initrddir}/xcyber360-server
fi

%preun

if [ $1 = 0 ]; then

  # Stop the services before uninstall the package
  # Check for systemd
  if command -v systemctl > /dev/null 2>&1 && systemctl > /dev/null 2>&1 && systemctl is-active --quiet xcyber360-server > /dev/null 2>&1; then
    systemctl stop xcyber360-server.service > /dev/null 2>&1
  # Check for SysV
  elif command -v service > /dev/null 2>&1 && service xcyber360-server status 2>/dev/null | grep "is running" > /dev/null 2>&1; then
    service xcyber360-server stop > /dev/null 2>&1
  else
    echo "Unable to stop xcyber360-server. Neither systemctl nor service are available."
  fi
fi

%postun

# If the package is been uninstalled
if [ $1 = 0 ];then
  # Remove the xcyber360 user if it exists
  if getent passwd xcyber360 > /dev/null 2>&1; then
    userdel xcyber360 >/dev/null 2>&1
  fi
  # Remove the xcyber360 group if it exists
  if command -v getent > /dev/null 2>&1 && getent group xcyber360 > /dev/null 2>&1; then
    groupdel xcyber360 >/dev/null 2>&1
  elif getent group xcyber360 > /dev/null 2>&1; then
    groupdel xcyber360 >/dev/null 2>&1
  fi

  # Remove lingering folders and files
  rm -rf %{_localstatedir}tmp/xcyber360-server
  rm -rf %{_localstatedir}usr/bin/xcyber360-engine
  rm -rf %{_localstatedir}usr/bin/xcyber360-apid
  rm -rf %{_localstatedir}usr/bin/xcyber360-comms-apid
  rm -rf %{_localstatedir}usr/bin/xcyber360-server
  rm -rf %{_localstatedir}run/xcyber360-server
  rm -rf %{_localstatedir}var/lib/xcyber360-server
  rm -rf %{_localstatedir}usr/share/xcyber360-server
  rm -rf %{_localstatedir}etc/xcyber360-server
fi

# posttrans code is the last thing executed in a install/upgrade
%posttrans
if [ -f %{_sysconfdir}/systemd/system/xcyber360-server.service ]; then
  rm -rf %{_sysconfdir}/systemd/system/xcyber360-server.service
  systemctl daemon-reload > /dev/null 2>&1
fi

if [ -f %{_localstatedir}/tmp/xcyber360.restart ]; then
  rm -f %{_localstatedir}/tmp/xcyber360.restart
  if command -v systemctl > /dev/null 2>&1 && systemctl > /dev/null 2>&1 ; then
    systemctl daemon-reload > /dev/null 2>&1
    systemctl restart xcyber360-server.service > /dev/null 2>&1
  elif command -v service > /dev/null 2>&1 ; then
    service xcyber360-server restart > /dev/null 2>&1
  fi
fi

chown -R root:xcyber360 %{_localstatedir}var/lib/xcyber360-server
find %{_localstatedir}var/lib/xcyber360-server -type d -exec chmod 750 {} \; -o -type f -exec chmod 640 {} \;
chown -R root:xcyber360 %{_localstatedir}var/log/xcyber360-server
find %{_localstatedir}var/log/xcyber360-server -type d -exec chmod 755 {} \; -o -type f -exec chmod 644 {} \;
chown -R root:xcyber360 %{_localstatedir}usr/share/xcyber360-server
find %{_localstatedir}usr/share/xcyber360-server -type d -exec chmod 755 {} \; -o -type f -exec chmod 644 {} \;
chown -R root:xcyber360 %{_localstatedir}etc/xcyber360-server
find %{_localstatedir}etc/xcyber360-server -type d -exec chmod 755 {} \; -o -type f -exec chmod 644 {} \;

# Fix Python permissions
chmod -R 0750 %{_localstatedir}usr/share/xcyber360-server/framework/python/bin

%triggerin -- glibc

%clean
rm -fr %{buildroot}

%files
%defattr(-,root,xcyber360)
%dir %attr(750, root, xcyber360) %{_localstatedir}run/xcyber360-server
%dir %attr(750, root, xcyber360) %{_localstatedir}var/lib/xcyber360-server
%dir %attr(750, root, xcyber360) %{_localstatedir}var/lib/xcyber360-server/vd
%dir %attr(750, root, xcyber360) %{_localstatedir}var/lib/xcyber360-server/engine
%dir %attr(750, root, xcyber360) %{_localstatedir}var/lib/xcyber360-server/engine/tzdb
%dir %attr(750, root, xcyber360) %{_localstatedir}var/log/xcyber360-server
%dir %attr(750, root, xcyber360) %{_localstatedir}var/log/xcyber360-server/engine
%dir %attr(750, root, xcyber360) %{_localstatedir}etc/xcyber360-server
%dir %attr(750, root, xcyber360) %{_localstatedir}etc/xcyber360-server/api
%dir %attr(750, root, xcyber360) %{_localstatedir}etc/xcyber360-server/cluster
%dir %attr(750, root, xcyber360) %{_localstatedir}etc/xcyber360-server/shared
%dir %attr(750, root, xcyber360) %{_localstatedir}run/xcyber360-server/cluster
%dir %attr(750, root, xcyber360) %{_localstatedir}run/xcyber360-server/socket
%dir %attr(750, root, xcyber360) %{_localstatedir}usr/share/xcyber360-server/lib
%dir %attr(750, root, xcyber360) %{_localstatedir}usr/share/xcyber360-server/framework
%dir %attr(750, root, xcyber360) %{_localstatedir}usr/share/xcyber360-server/api
%dir %attr(750, root, xcyber360) %{_localstatedir}usr/share/xcyber360-server/apis
%{_localstatedir}var/lib/xcyber360-server/engine/tzdb/*
%{_localstatedir}etc/xcyber360-server/*
%{_localstatedir}usr/share/xcyber360-server/lib/*
%{_localstatedir}usr/share/xcyber360-server/framework/*
%{_localstatedir}usr/share/xcyber360-server/api/*
%{_localstatedir}usr/share/xcyber360-server/apis/*
%dir %attr(750, root, xcyber360) %{_localstatedir}var/lib/xcyber360-server/engine/store
%{_localstatedir}var/lib/xcyber360-server/engine/store/*
%dir %attr(750, root, xcyber360) %{_localstatedir}var/lib/xcyber360-server/engine/kvdb
%{_localstatedir}var/lib/xcyber360-server/engine/kvdb/*
%dir %attr(750, root, xcyber360) %{_localstatedir}var/lib/xcyber360-server/indexer-connector

%attr(750, root, xcyber360) %{_localstatedir}usr/bin/xcyber360-engine
%attr(750, root, xcyber360) %{_localstatedir}usr/bin/xcyber360-apid
%attr(750, root, xcyber360) %{_localstatedir}usr/bin/xcyber360-comms-apid
%attr(750, root, xcyber360) %{_localstatedir}usr/bin/xcyber360-server
%attr(640, root, xcyber360) %{_localstatedir}tmp/xcyber360-server/vd_1.0.0_vd_4.10.0.tar.xz
%attr(640, root, xcyber360) %{_localstatedir}tmp/xcyber360-server/engine_store_0.0.2_5.0.0.tar.gz

%config(missingok) %{_initrddir}/xcyber360-server
/usr/lib/systemd/system/xcyber360-server.service

%changelog
* Mon Jun 2 2025 support <info@xcyber360.com> - 5.0.0
- More info: https://documentation.xcyber360.com/current/release-notes/release-5-0-0.html
