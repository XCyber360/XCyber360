"""
Module to build the Xcyber360 socket paths.

This modules contains the following:

- SocketPath(Xcyber360Path:
    - get_analysisd_socket_path
    - get_queue_socket_path
    - get_authd_socket_path
    - get_execd_socket_path
    - get_logcollectord_socket_path
    - get_monitord_socket_path
    - get_logtest_socket_path
    - get_remoted_socket_path
    - get_syscheckd_socket_path
    - get_modulesd_socket_path
    - get_modulesd_download_socket_path
    - get_modulesd_control_socket_path
    - get_csyslogd_socket_path
    - get_request_socket_path
"""

import sys
import os

from xcyber360_qa_framework.global_variables.path.xcyber360_path import Xcyber360Path


class SocketPath(Xcyber360Path):
    """Class to build the xcyber360 socket paths.

    Args:
        os_system (str): Operating system.

    Attributes:
        os_system (str): Operating system.
        sockets_path (str): Xcyber360 logs path.
    """
    def __init__(self, os_system=sys.platform):
        super().__init__(os_system)
        self.sockets_path = os.path.join(self.get_xcyber360_path(), 'queue', 'sockets')

    def get_analysisd_socket_path(self):
        return os.path.join(self.sockets_path, 'analysis')

    def get_queue_socket_path(self):
        return os.path.join(self.sockets_path, 'queue')

    def get_authd_socket_path(self):
        return os.path.join(self.sockets_path, 'auth')

    def get_execd_socket_path(self):
        return os.path.join(self.sockets_path, 'com')

    def get_logcollectord_socket_path(self):
        return os.path.join(self.sockets_path, 'logcollector')

    def get_monitord_socket_path(self):
        return os.path.join(self.sockets_path, 'monitor')

    def get_logtest_socket_path(self):
        return os.path.join(self.sockets_path, 'logtest')

    def get_remoted_socket_path(self):
        return os.path.join(self.sockets_path, 'remote')

    def get_syscheckd_socket_path(self):
        return os.path.join(self.sockets_path, 'syscheck')

    def get_modulesd_socket_path(self):
        return os.path.join(self.sockets_path, 'wmodules')

    def get_modulesd_download_socket_path(self):
        return os.path.join(self.sockets_path, 'download')

    def get_modulesd_control_socket_path(self):
        return os.path.join(self.sockets_path, 'control')

    def get_csyslogd_socket_path(self):
        return os.path.join(self.sockets_path, 'csyslogd')

    def get_request_socket_path(self):
        return os.path.join(self.sockets_path, 'request')
