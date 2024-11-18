

import json
import os
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor
from contextvars import ContextVar
from copy import deepcopy
from functools import lru_cache, wraps
from grp import getgrnam
from multiprocessing import Event
from pathlib import Path
from pwd import getpwnam
from typing import Any, Dict


# ===================================================== Functions ======================================================
@lru_cache(maxsize=None)
def find_xcyber360_path() -> str:
    """Get the Xcyber360 installation path.

    Returns
    -------
    str
        Path where Xcyber360 is installed or empty string if there is no framework in the environment.
    """
    abs_path = os.path.abspath(os.path.dirname(__file__))
    allparts = []
    while 1:
        parts = os.path.split(abs_path)
        if parts[0] == abs_path:  # sentinel for absolute paths.
            allparts.insert(0, parts[0])
            break
        elif parts[1] == abs_path:  # sentinel for relative paths.
            allparts.insert(0, parts[1])
            break
        else:
            abs_path = parts[0]
            allparts.insert(0, parts[1])

    xcyber360_path = ''
    try:
        for i in range(0, allparts.index('framework')):
            xcyber360_path = os.path.join(xcyber360_path, allparts[i])
    except ValueError:
        pass

    return xcyber360_path


def xcyber360_uid() -> int:
    """Retrieve the numerical user ID for the xcyber360 user.

    Returns
    -------
    int
        Numerical user ID.
    """
    return getpwnam(USER_NAME).pw_uid if globals()['_XCYBER360_UID'] is None else globals()['_XCYBER360_UID']


def xcyber360_gid() -> int:
    """Retrieve the numerical group ID for the xcyber360 group.

    Returns
    -------
    int
        Numerical group ID.
    """
    return getgrnam(GROUP_NAME).gr_gid if globals()['_XCYBER360_GID'] is None else globals()['_XCYBER360_GID']


def async_context_cached(key: str = '') -> Any:
    """Save the result of the asynchronous decorated function in a cache.

    Next calls to the asynchronous decorated function returns the saved result saving time and resources. The cache gets
    invalidated at the end of the request.

    Parameters
    ----------
    key : str
        Part of the cache entry identifier. The identifier will be the key + args + kwargs.

    Returns
    -------
    Any
        The result of the first call to the asynchronous decorated function.

    Notes
    -----
    The returned object will be a deep copy of the cached one.
    """

    def decorator(func) -> Any:
        @wraps(func)
        async def wrapper(*args, **kwargs) -> Any:
            cached_key = json.dumps({'key': key, 'args': args, 'kwargs': kwargs})
            if cached_key not in _context_cache:
                _context_cache[cached_key] = ContextVar(cached_key, default=None)
            if _context_cache[cached_key].get() is None:
                result = await func(*args, **kwargs)
                _context_cache[cached_key].set(result)
            return deepcopy(_context_cache[cached_key].get())

        return wrapper

    return decorator


def context_cached(key: str = '') -> Any:
    """Save the result of the decorated function in a cache.

    Next calls to the decorated function returns the saved result saving time and resources. The cache gets
    invalidated at the end of the request.

    Parameters
    ----------
    key : str
        Part of the cache entry identifier. The identifier will be the key + args + kwargs.

    Returns
    -------
    Any
        The result of the first call to the decorated function.

    Notes
    -----
    The returned object will be a deep copy of the cached one.
    """

    def decorator(func) -> Any:
        @wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            cached_key = json.dumps({'key': key, 'args': args, 'kwargs': kwargs})
            if cached_key not in _context_cache:
                _context_cache[cached_key] = ContextVar(cached_key, default=None)
            if _context_cache[cached_key].get() is None:
                result = func(*args, **kwargs)
                _context_cache[cached_key].set(result)
            return deepcopy(_context_cache[cached_key].get())

        return wrapper

    return decorator


def reset_context_cache() -> None:
    """Reset context cache."""

    for context_var in _context_cache.values():
        context_var.set(None)


def get_context_cache() -> dict:
    """Get the context cache.

    Returns
    -------
    dict
        Dictionary with the context variables representing the cache.
    """

    return _context_cache


# ================================================= Context variables ==================================================
rbac: ContextVar[Dict] = ContextVar('rbac', default={'rbac_mode': 'black'})
current_user: ContextVar[str] = ContextVar('current_user', default='')
broadcast: ContextVar[bool] = ContextVar('broadcast', default=False)
cluster_nodes: ContextVar[list] = ContextVar('cluster_nodes', default=list())
origin_module: ContextVar[str] = ContextVar('origin_module', default='framework')
try:
    mp_pools: ContextVar[Dict] = ContextVar('mp_pools', default={
        'process_pool': ProcessPoolExecutor(max_workers=1),
        'authentication_pool': ProcessPoolExecutor(max_workers=1),
        'events_pool': ProcessPoolExecutor(max_workers=1)
    })
# Handle exception when the user running Xcyber360 cannot access /dev/shm.
except (FileNotFoundError, PermissionError):
    mp_pools: ContextVar[Dict] = ContextVar('mp_pools', default={
        'thread_pool': ThreadPoolExecutor(max_workers=1)
    })
_context_cache = dict()


# =========================================== Xcyber360 constants and variables ============================================
# Clear cache event.
cache_event = Event()
_XCYBER360_UID = None
_XCYBER360_GID = None
GROUP_NAME = 'xcyber360'
USER_NAME = 'xcyber360'

# TODO: Keep until we remove the different deprecated functionalities that are importing it.
XCYBER360_PATH = ''

USR_ROOT = Path('/usr')
ETC_ROOT = Path('/etc')
RUN_ROOT = Path('/run')
VAR_ROOT = Path('/var')
BIN_ROOT = Path('/bin')

USR_SHARE = USR_ROOT / Path('share')
VAR_LOG = VAR_ROOT / Path('log')
VAR_LIB = VAR_ROOT / Path('lib')

XCYBER360_SERVER = 'xcyber360-server'
XCYBER360_SHARE = USR_SHARE / XCYBER360_SERVER
XCYBER360_ETC = ETC_ROOT / XCYBER360_SERVER
XCYBER360_RUN = RUN_ROOT / XCYBER360_SERVER
XCYBER360_LOG = VAR_LOG / XCYBER360_SERVER
XCYBER360_LIB = VAR_LIB / XCYBER360_SERVER

XCYBER360_QUEUE = XCYBER360_RUN / 'cluster'
XCYBER360_SOCKET = XCYBER360_RUN / 'socket'

XCYBER360_SHARED = XCYBER360_ETC / 'shared'

LOCAL_SERVER_SOCKET = 'local-server.sock'


# ============================================= Xcyber360 constants - Commands =============================================
CHECK_CONFIG_COMMAND = 'check-manager-configuration'
RESTART_XCYBER360_COMMAND = 'restart-xcyber360'


# =========================================== Xcyber360 constants - Date format ============================================
DATE_FORMAT = "%Y-%m-%dT%H:%M:%SZ"
DECIMALS_DATE_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


# ============================================ Xcyber360 constants - Extensions ============================================
RULES_EXTENSION = '.xml'
DECODERS_EXTENSION = '.xml'
LISTS_EXTENSION = ''
COMPILED_LISTS_EXTENSION = '.cdb'


# ========================================= Xcyber360 constants - Size and limits ==========================================
MAX_SOCKET_BUFFER_SIZE = 64 * 1024  # 64KB.
MAX_QUERY_FILTERS_RESERVED_SIZE = MAX_SOCKET_BUFFER_SIZE - 4 * 1024  # MAX_BUFFER_SIZE - 4KB.
AGENT_NAME_LEN_LIMIT = 128
DATABASE_LIMIT = 500
MAXIMUM_DATABASE_LIMIT = 100000
MAX_GROUPS_PER_MULTIGROUP = 128


# ============================================= Xcyber360 constants - Version ==============================================
# Agent upgrading variables.
WPK_REPO_URL_4_X = "packages.xcyber360.com/4.x/wpk/"
# Agent component stats required version.
AGENT_COMPONENT_STATS_REQUIRED_VERSION = {'logcollector': 'v4.2.0', 'agent': 'v4.2.0'}
# Version variables (legacy, required, etc).
AR_LEGACY_VERSION = 'Xcyber360 v4.2.0'
ACTIVE_CONFIG_VERSION = 'Xcyber360 v3.7.0'


# ================================================ Xcyber360 path - Config =================================================
# TODO: Keep until we remove the different functionalities completely
AR_CONF = ''
CLIENT_KEYS = ''
XCYBER360_SERVER_YML = XCYBER360_ETC / 'xcyber360-server.yml'


# ================================================= Xcyber360 path - Misc ==================================================
DEFAULT_RBAC_RESOURCES = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'rbac', 'default')

# TODO: Constants asociate to functionality next to deprecate.
XCYBER360_LOG_JSON = os.path.join('', 'ossec.json')
ANALYSISD_STATS = os.path.join(XCYBER360_PATH, 'var', 'run', 'xcyber360-analysisd.state')
REMOTED_STATS = os.path.join(XCYBER360_PATH, 'var', 'run', 'xcyber360-remoted.state')
OSSEC_TMP_PATH = os.path.join(XCYBER360_PATH, 'tmp')
WDB_PATH = os.path.join(XCYBER360_PATH, 'queue', 'db')
STATS_PATH = os.path.join(XCYBER360_PATH, 'stats')


# ================================================ Xcyber360 path - Sockets ================================================
ENGINE_SOCKET = XCYBER360_RUN / 'engine.socket'
# TODO: Constants asociated to functionality next to deprecate.
ANALYSISD_SOCKET = os.path.join(XCYBER360_PATH, 'queue', 'sockets', 'analysis')
AR_SOCKET = os.path.join(XCYBER360_PATH, 'queue', 'alerts', 'ar')
EXECQ_SOCKET = os.path.join(XCYBER360_PATH, 'queue', 'alerts', 'execq')
AUTHD_SOCKET = os.path.join(XCYBER360_PATH, 'queue', 'sockets', 'auth')
WCOM_SOCKET = os.path.join(XCYBER360_PATH, 'queue', 'sockets', 'com')
LOGTEST_SOCKET = os.path.join(XCYBER360_PATH, 'queue', 'sockets', 'logtest')
UPGRADE_SOCKET = os.path.join(XCYBER360_PATH, 'queue', 'tasks', 'upgrade')
REMOTED_SOCKET = os.path.join(XCYBER360_PATH, 'queue', 'sockets', 'remote')
TASKS_SOCKET = os.path.join(XCYBER360_PATH, 'queue', 'tasks', 'task')
WDB_SOCKET = os.path.join(XCYBER360_PATH, 'queue', 'db', 'wdb')
WMODULES_SOCKET = os.path.join(XCYBER360_PATH, 'queue', 'sockets', 'wmodules')
QUEUE_SOCKET = os.path.join(XCYBER360_PATH, 'queue', 'sockets', 'queue')


# ================================================ Xcyber360 path - Ruleset ================================================
# TODO: Constants asociated to functionality next to deprecate.
RULESET_PATH = os.path.join(XCYBER360_PATH, 'ruleset')
RULES_PATH = os.path.join(RULESET_PATH, 'rules')
DECODERS_PATH = os.path.join(RULESET_PATH, 'decoders')
LISTS_PATH = os.path.join(RULESET_PATH, 'lists')
USER_LISTS_PATH = os.path.join(XCYBER360_PATH, 'etc', 'lists')
USER_RULES_PATH = os.path.join(XCYBER360_PATH, 'etc', 'rules')
USER_DECODERS_PATH = os.path.join(XCYBER360_PATH, 'etc', 'decoders')
