# Syntax: make [ all | build | install | examples | clean ]

XCYBER360_GROUP       = xcyber360
XCYBER360_SERVER	  = xcyber360-server

SHARE_INSTALLDIR       ?= /usr/share/${XCYBER360_SERVER}
LOG_INSTALLDIR         ?= /var/log/${XCYBER360_SERVER}
LIB_INSTALLDIR         ?= /var/lib/${XCYBER360_SERVER}
ETC_INSTALLDIR         ?= /etc/${XCYBER360_SERVER}
RUN_INSTALLDIR         ?= /run/${XCYBER360_SERVER}
BIN_INSTALLDIR         ?= /bin

CC           = gcc
CFLAGS       = -pipe -Wall -Wextra
THREAD_FLAGS = -pthread
MV_FILE      = mv -f
RM_FILE      = rm -f
INSTALL_DIR  = install -o root -g ${XCYBER360_GROUP} -m 0750  -d
INSTALL_EXEC = install -o root -g ${XCYBER360_GROUP} -m 0750
INSTALL_FILE = install -o root -g ${XCYBER360_GROUP} -m 0640

ifdef DEBUG
	CFLAGS+=-g -I ../src
	LFLAGS+=-g
else
	CFLAGS+=-O2 -I ../src
	LFLAGS+=-O2
endif

.PHONY: all build install examples clean

all: build

install:
	# SHARE
	$(INSTALL_DIR) $(SHARE_INSTALLDIR)/framework
	$(INSTALL_DIR) $(SHARE_INSTALLDIR)/framework/scripts
	$(INSTALL_DIR) $(SHARE_INSTALLDIR)/framework/xcyber360
	$(INSTALL_DIR) $(SHARE_INSTALLDIR)/framework/xcyber360/core/cluster
	$(INSTALL_DIR) $(SHARE_INSTALLDIR)/framework/xcyber360/core/cluster/dapi
	$(INSTALL_DIR) $(SHARE_INSTALLDIR)/framework/xcyber360/core/cluster/hap_helper

	# LOGS
	$(INSTALL_DIR) $(LOG_INSTALLDIR)

	# ETC
	$(INSTALL_DIR) $(ETC_INSTALLDIR)
	$(INSTALL_DIR) $(ETC_INSTALLDIR)/cluster
	$(INSTALL_DIR) $(ETC_INSTALLDIR)/shared

	# RUN
	$(INSTALL_DIR) $(RUN_INSTALLDIR)
	$(INSTALL_DIR) $(RUN_INSTALLDIR)/cluster
	$(INSTALL_DIR) $(RUN_INSTALLDIR)/socket

	# SHARE
	$(INSTALL_FILE) scripts/*.py ${SHARE_INSTALLDIR}/framework/scripts
	$(INSTALL_FILE) xcyber360/*.py ${SHARE_INSTALLDIR}/framework/xcyber360
	$(INSTALL_FILE) xcyber360/core/cluster/*.py ${SHARE_INSTALLDIR}/framework/xcyber360/core/cluster
	$(INSTALL_FILE) xcyber360/core/cluster/dapi/*.py ${SHARE_INSTALLDIR}/framework/xcyber360/core/cluster/dapi
	$(INSTALL_FILE) xcyber360/core/cluster/hap_helper/*.py ${SHARE_INSTALLDIR}/framework/xcyber360/core/cluster/hap_helper

	# ETC
	$(INSTALL_FILE) ../etc/xcyber360-server.yml ${ETC_INSTALLDIR}


	# BIN
#	Install scripts/%.py on $(INSTALLDIR)/bin/%
	$(foreach script,$(wildcard scripts/*.py),$(INSTALL_EXEC) wrappers/generic_wrapper.sh $(patsubst scripts/%.py,${BIN_INSTALLDIR}/%,$(script));)
#   Provisional name change for xcyber360-logtest and xcyber360-clusterd
	$(MV_FILE) ${BIN_INSTALLDIR}/xcyber360_server ${BIN_INSTALLDIR}/xcyber360-server
	$(RM_FILE) ${BIN_INSTALLDIR}/__init__

examples: install
	$(INSTALL_DIR) $(INSTALLDIR)/framework/examples
	$(INSTALL_EXEC) examples/*.py ${INSTALLDIR}/framework/examples

clean:
	$(RM_FILE) $(BUILD_TARGET) *.o *.so.0
