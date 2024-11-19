"""
Module to build the Xcyber360 binary paths according to the selected operating system.

This modules contains the following:

- BinaryPath(Xcyber360Path):
    - get_binary_path
    - get_agent_control_path
    - get_agent_groups_path
    - get_agent_upgrade_path
    - get_clear_stats_path
    - get_cluster_control_path
    - get_manage_agents_path
    - get_xcyber360_control_path
    - get_xcyber360_agentlessd_path
    - get_xcyber360_analysisd_path
    - get_xcyber360_apid_path
    - get_xcyber360_authd_path
    - get_xcyber360_clusterd_path
    - get_xcyber360_csyslogd_path
    - get_xcyber360_db_path
    - get_xcyber360_dbd_path
    - get_xcyber360_execd_path
    - get_xcyber360_integratord_path
    - get_xcyber360_logcollector_path
    - get_xcyber360_logtest_path
    - get_xcyber360_maild_path
    - get_xcyber360_modulesd_path
    - get_xcyber360_monitord_path
    - get_xcyber360_regex_path
    - get_xcyber360_remoted_path
    - get_xcyber360_reportd_path
    - get_xcyber360_syscheckd_path
    - get_agent_auth_path
    - get_xcyber360_agentd_path
"""

import sys
import os

from xcyber360_qa_framework.global_variables.path.xcyber360_path import Xcyber360Path
from xcyber360_qa_framework.global_variables.platform import WINDOWS


class BinaryPath(Xcyber360Path):
    """Class to build the xcyber360 binary paths according to the selected OS.

    Args:
        os_system (str): Operating system.

    Attributes:
        os_system (str): Operating system.
        binary_path (str): Xcyber360 binary paths.
    """
    def __init__(self, os_system=sys.platform):
        super().__init__(os_system=os_system)
        self.binary_path = os.path.join(self.get_xcyber360_path()) if os_system == WINDOWS else \
            os.path.join(self.get_xcyber360_path, 'bin')

    def get_binary_path(self):
        return self.binary_path

    def get_agent_control_path(self):
        return os.path.join(self.binary_path, 'agent_control')

    def get_agent_groups_path(self):
        return os.path.join(self.binary_path, 'agent_groups')

    def get_agent_upgrade_path(self):
        return os.path.join(self.binary_path, 'agent_upgrade')

    def get_clear_stats_path(self):
        return os.path.join(self.binary_path, 'clear_stats')

    def get_cluster_control_path(self):
        return os.path.join(self.binary_path, 'cluster_control')

    def get_manage_agents_path(self):
        return os.path.join(self.binary_path, 'manage_agents')

    def get_xcyber360_control_path(self):
        return os.path.join(self.binary_path, 'xcyber360_control')

    def get_xcyber360_agentlessd_path(self):
        return os.path.join(self.binary_path, 'xcyber360-agentlessd')

    def get_xcyber360_analysisd_path(self):
        return os.path.join(self.binary_path, 'xcyber360-analysisd')

    def get_xcyber360_apid_path(self):
        return os.path.join(self.binary_path, 'xcyber360-apid')

    def get_xcyber360_authd_path(self):
        return os.path.join(self.binary_path, 'xcyber360-authd')

    def get_xcyber360_clusterd_path(self):
        return os.path.join(self.binary_path, 'xcyber360-clusterd')

    def get_xcyber360_csyslogd_path(self):
        return os.path.join(self.binary_path, 'xcyber360-csyslogd')

    def get_xcyber360_db_path(self):
        return os.path.join(self.binary_path, 'xcyber360-db')

    def get_xcyber360_dbd_path(self):
        return os.path.join(self.binary_path, 'xcyber360-dbd')

    def get_xcyber360_execd_path(self):
        return os.path.join(self.binary_path, 'xcyber360-execd')

    def get_xcyber360_integratord_path(self):
        return os.path.join(self.binary_path, 'xcyber360-integratord')

    def get_xcyber360_logcollector_path(self):
        return os.path.join(self.binary_path, 'xcyber360-logcollector')

    def get_xcyber360_logtest_path(self):
        return os.path.join(self.binary_path, 'xcyber360-logtest')

    def get_xcyber360_maild_path(self):
        return os.path.join(self.binary_path, 'xcyber360-maild')

    def get_xcyber360_modulesd_path(self):
        return os.path.join(self.binary_path, 'xcyber360-modulesd')

    def get_xcyber360_monitord_path(self):
        return os.path.join(self.binary_path, 'xcyber360-monitord')

    def get_xcyber360_regex_path(self):
        return os.path.join(self.binary_path, 'xcyber360-regex')

    def get_xcyber360_remoted_path(self):
        return os.path.join(self.binary_path, 'xcyber360-remoted')

    def get_xcyber360_reportd_path(self):
        return os.path.join(self.binary_path, 'xcyber360-reportd')

    def get_xcyber360_syscheckd_path(self):
        return os.path.join(self.binary_path, 'xcyber360-syscheckd')

    def get_agent_auth_path(self):
        return os.path.join(self.binary_path, 'agent-auth')

    def get_xcyber360_agentd_path(self):
        return os.path.join(self.binary_path, 'xcyber360-agentd')
