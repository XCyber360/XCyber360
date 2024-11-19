"""
Module to build the Xcyber360 path according to the selected operating system.

This modules contains the following:

- Xcyber360Path:
    - get_xcyber360_path
"""

import sys
import os

from xcyber360_qa_framework.global_variables.platform import WINDOWS, MACOS


class Xcyber360Path:
    """Class to build the xcyber360 paths according to the selected OS.

    Args:
        os_system (str): Operating system.

    Attributes:
        os_system (str): Operating system.
    """
    def __init__(self, os_system=sys.platform):
        self.os_system = os_system

    def get_xcyber360_path(self):
        """Get the xcyber360 path.

        Returns:
            str: Xcyber360 path.
        """
        if self.os_system == WINDOWS:
            return os.path.join('C:', os.sep, 'Program Files (x86)', 'ossec-agent')
        elif self.os_system == MACOS:
            return os.path.join('/', 'Library', 'Ossec')
        else:
            return os.path.join('/var', 'ossec')
