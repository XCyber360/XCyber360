"""
Module to build the Xcyber360 config paths according to the selected operating system.

This modules contains the following:

- ConfigPath(Xcyber360Path):
    - get_xcyber360_config_path
    - get_xcyber360_config_file_path
    - get_internal_config_file_path
    - get_local_internal_config_file_path
    - get_client_keys_file_path
    - get_ssl_manager_cert_file_path
    - get_local_decoders_file_path
    - get_local_rules_file_path
    - get_default_agent_conf_file_path
"""
import sys
import os

from xcyber360_qa_framework.global_variables.path.xcyber360_path import Xcyber360Path
from xcyber360_qa_framework.global_variables.platform import WINDOWS


class ConfigPath(Xcyber360Path):
    """Class to build the xcyber360 config paths according to the selected OS.

    Args:
        os_system (str): Operating system.

    Attributes:
        os_system (str): Operating system.
        config_path (str): Xcyber360 config files path.
    """
    def __init__(self, os_system=sys.platform):
        super().__init__(os_system=os_system)
        self.config_path = os.path.join(self.get_xcyber360_path()) if os_system == WINDOWS else \
            os.path.join(self.get_xcyber360_path, 'etc')

    def get_xcyber360_config_path(self):
        return self.config_path

    def get_xcyber360_config_file_path(self):
        return os.path.join(self.config_path, 'ossec.conf')

    def get_internal_config_file_path(self):
        return os.path.join(self.config_path, 'internal_options.conf')

    def get_local_internal_config_file_path(self):
        return os.path.join(self.config_path, 'local_internal_options.conf')

    def get_client_keys_file_path(self):
        return os.path.join(self.config_path, 'client.keys')

    def get_ssl_manager_cert_file_path(self):
        return os.path.join(self.config_path, 'sslmanager.cert')

    def get_local_decoders_file_path(self):
        return os.path.join(self.config_path, 'decoders', 'local_decoder.xml')

    def get_local_rules_file_path(self):
        return os.path.join(self.config_path, 'rules', 'local_rules.xml')

    def get_default_agent_conf_file_path(self):
        return os.path.join(self.config_path, 'shared', 'default', 'agent.conf')
