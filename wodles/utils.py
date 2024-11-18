

import os
import subprocess
from functools import lru_cache
from sys import exit


@lru_cache(maxsize=None)
def find_xcyber360_path() -> str:
    """
    Get the Xcyber360 installation path.

    Returns
    -------
    str
        Path where Xcyber360 is installed or empty string if there is no framework in the environment.
    """
    abs_path = os.path.abspath(os.path.dirname(__file__))
    allparts = []
    while 1:
        parts = os.path.split(abs_path)
        if parts[0] == abs_path:  # sentinel for absolute paths
            allparts.insert(0, parts[0])
            break
        elif parts[1] == abs_path:  # sentinel for relative paths
            allparts.insert(0, parts[1])
            break
        else:
            abs_path = parts[0]
            allparts.insert(0, parts[1])

    xcyber360_path = ''
    try:
        for i in range(0, allparts.index('wodles')):
            xcyber360_path = os.path.join(xcyber360_path, allparts[i])
    except ValueError:
        pass

    return xcyber360_path


def call_xcyber360_control(option: str) -> str:
    """
    Execute the xcyber360-control script with the parameters specified.

    Parameters
    ----------
    option : str
        The option that will be passed to the script.

    Returns
    -------
    str
        The output of the call to xcyber360-control.
    """
    xcyber360_control = os.path.join(find_xcyber360_path(), "bin", "xcyber360-control")
    try:
        proc = subprocess.Popen([xcyber360_control, option], stdout=subprocess.PIPE)
        (stdout, stderr) = proc.communicate()
        return stdout.decode()
    except (OSError, ChildProcessError):
        print(f'ERROR: a problem occurred while executing {xcyber360_control}')
        exit(1)


def get_xcyber360_info(field: str) -> str:
    """
    Execute the xcyber360-control script with the 'info' argument, filtering by field if specified.

    Parameters
    ----------
    field : str
        The field of the output that's being requested. Its value can be 'XCYBER360_VERSION', 'XCYBER360_REVISION' or
        'XCYBER360_TYPE'.

    Returns
    -------
    str
        The output of the xcyber360-control script.
    """
    xcyber360_info = call_xcyber360_control("info")
    if not xcyber360_info:
        return "ERROR"

    if not field:
        return xcyber360_info

    env_variables = xcyber360_info.rsplit("\n")
    env_variables.remove("")
    xcyber360_env_vars = dict()
    for env_variable in env_variables:
        key, value = env_variable.split("=")
        xcyber360_env_vars[key] = value.replace("\"", "")

    return xcyber360_env_vars[field]


@lru_cache(maxsize=None)
def get_xcyber360_version() -> str:
    """
    Return the version of Xcyber360 installed.

    Returns
    -------
    str
        The version of Xcyber360 installed.
    """
    return get_xcyber360_info("XCYBER360_VERSION")


ANALYSISD = os.path.join(find_xcyber360_path(), 'queue', 'sockets', 'queue')
# Max size of the event that ANALYSISID can handle
MAX_EVENT_SIZE = 65535
