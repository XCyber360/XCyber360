# Makefile for Xcyber360 API

# May 3, 2017
#
# Syntax: make [ all | backup | install | restore | service ]

XCYBER360_GROUP       = xcyber360
XCYBER360_SERVER      = xcyber360-server
SHARE_INSTALLDIR  ?= /usr/share/${XCYBER360_SERVER}
ETC_INSTALLDIR    ?= /etc/${XCYBER360_SERVER}
BIN_INSTALLDIR    ?= /bin


MV_FILE        = mv -f
RM_FILE        = rm -f
INSTALL_DIR    = install -o root -g ${XCYBER360_GROUP} -m 0750 -d
INSTALL_RW_DIR = install -o root -g ${XCYBER360_GROUP} -m 0770 -d
INSTALL_EXEC   = install -o root -g ${XCYBER360_GROUP} -m 0750
INSTALL_FILE   = install -o root -g ${XCYBER360_GROUP} -m 0640
INSTALL_CONFIG_FILE   = install -o root -g ${XCYBER360_GROUP} -m 0660
PYTHON_BIN     = $(SHARE_INSTALLDIR)/framework/python/bin/python3


.PHONY: install

install:
    # Copy files and create folders
	# ETC
	$(INSTALL_DIR) $(ETC_INSTALLDIR)/api
	$(INSTALL_RW_DIR) $(ETC_INSTALLDIR)/api/configuration
	$(INSTALL_RW_DIR) $(ETC_INSTALLDIR)/api/configuration/ssl
	$(INSTALL_RW_DIR) $(ETC_INSTALLDIR)/api/configuration/security


	# SHARE
	$(INSTALL_DIR) $(SHARE_INSTALLDIR)/api/scripts
	$(INSTALL_FILE) scripts/xcyber360_apid.py ${SHARE_INSTALLDIR}/api/scripts

    # Install scripts/%.py on $(INSTALLDIR)/bin/%
	$(foreach script,$(wildcard scripts/*.py),$(INSTALL_EXEC) api/wrappers/generic_wrapper.sh $(patsubst scripts/%.py,${BIN_INSTALLDIR}/%,$(script));)

	$(MV_FILE) ${BIN_INSTALLDIR}/xcyber360_apid ${BIN_INSTALLDIR}/xcyber360-apid
