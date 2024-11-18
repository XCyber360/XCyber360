# Makefile for Xcyber360 APIs
# Copyright (C) 2015, Xcyber360 Inc.
# May 3, 2017
#
# Syntax: make [ all | install | service ]

XCYBER360_GROUP       = xcyber360
XCYBER360_SERVER      = xcyber360-server
SHARE_INSTALLDIR  ?= /usr/share/${XCYBER360_SERVER}
ETC_INSTALLDIR    ?= /etc/${XCYBER360_SERVER}
BIN_INSTALLDIR    ?= /bin

MV_FILE        = mv -f
INSTALL_DIR    = install -o root -g ${XCYBER360_GROUP} -m 0750 -d
INSTALL_EXEC   = install -o root -g ${XCYBER360_GROUP} -m 0750
INSTALL_FILE   = install -o root -g ${XCYBER360_GROUP} -m 0640


.PHONY: all install

all: install

install:

	$(INSTALL_DIR) $(SHARE_INSTALLDIR)/apis/scripts
	$(INSTALL_FILE) scripts/xcyber360_comms_apid.py ${SHARE_INSTALLDIR}/apis/scripts

    # Install scripts/%.py on $(INSTALLDIR)/bin/%
	$(foreach script,$(wildcard scripts/*.py),$(INSTALL_EXEC) wrappers/generic_wrapper.sh $(patsubst scripts/%.py,${BIN_INSTALLDIR}/%,$(script));)

	$(MV_FILE) ${BIN_INSTALLDIR}/xcyber360_comms_apid ${BIN_INSTALLDIR}/xcyber360-comms-apid
