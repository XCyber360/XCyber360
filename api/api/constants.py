

# This program is a free software; you can redistribute it and/or modify it under the terms of GPLv2

from xcyber360.core import common

API = 'api'
API_PATH = common.XCYBER360_SHARE / API
CONFIG_PATH = common.XCYBER360_ETC / API / 'configuration'
CONFIG_FILE_PATH = CONFIG_PATH / 'api.yaml'
SECURITY_PATH = CONFIG_PATH / 'security'
SECURITY_CONFIG_PATH = SECURITY_PATH / 'security.yaml'

API_LOG_PATH = common.XCYBER360_LOG / API
COMMS_API_LOG_PATH = common.XCYBER360_LOG / 'comms_api'
API_SSL_PATH = CONFIG_PATH / 'ssl'
INSTALLATION_UID_PATH = common.XCYBER360_LIB / 'installation_uid'
INSTALLATION_UID_KEY = 'installation_uid'
UPDATE_INFORMATION_KEY = 'update_information'
