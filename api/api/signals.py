
import asyncio
import contextlib
import logging
import os
import uuid
from functools import wraps
from typing import Callable

from connexion import ConnexionMiddleware
from xcyber360.core import common
from xcyber360.core.cluster.utils import running_in_master_node
from xcyber360.core.configuration import update_check_is_enabled
from xcyber360.core.manager import query_update_check_service
from xcyber360.core.config.client import CentralizedConfig

from api.constants import (
    INSTALLATION_UID_KEY,
    INSTALLATION_UID_PATH,
    UPDATE_INFORMATION_KEY,
)

ONE_DAY_SLEEP = 60*60*24

logger = logging.getLogger('xcyber360-api')

cti_context = {}


def cancel_signal_handler(func: Callable) -> Callable:
    """Decorator to handle asyncio.CancelledError for signals coroutines.

    Parameters
    ----------
    func : Callable
        Coroutine to handle.

    Returns
    -------
    Callable
        Wrapped coroutine with exception handled.
    """

    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            await func(*args, **kwargs)
        except asyncio.CancelledError:
            pass
    return wrapper


@cancel_signal_handler
async def check_installation_uid() -> None:
    """Check if the installation UID exists, populate it if not and inject it into the global cti context."""

    global cti_context
    if os.path.exists(INSTALLATION_UID_PATH):
        logger.info("Getting installation UID...")
        with open(INSTALLATION_UID_PATH, 'r') as file:
            installation_uid = file.readline()
    else:
        logger.info("Populating installation UID...")
        installation_uid = str(uuid.uuid4())
        with open(INSTALLATION_UID_PATH, 'w') as file:
            file.write(installation_uid)
            os.chown(file.name, common.xcyber360_uid(), common.xcyber360_gid())
            os.chmod(file.name, 0o660)
    cti_context[INSTALLATION_UID_KEY] = installation_uid


@cancel_signal_handler
async def get_update_information() -> None:
    """Get updates information from Update Check Service and inject into the global cti context."""

    global cti_context
    while True:
        logger.info('Getting updates information...')
        cti_context[UPDATE_INFORMATION_KEY] = await query_update_check_service(cti_context[INSTALLATION_UID_KEY])
        await asyncio.sleep(ONE_DAY_SLEEP)


@contextlib.asynccontextmanager
async def lifespan_handler(_: ConnexionMiddleware):
    """Logs the API startup/shutdown messages, register background tasks and initialize indexer client."""

    tasks: list[asyncio.Task] = []

    if running_in_master_node():
        tasks.append(asyncio.create_task(check_installation_uid()))
        if update_check_is_enabled():
            tasks.append(asyncio.create_task(get_update_information()))

    # Log the initial server startup message.
    management_api_config = CentralizedConfig.get_management_api_config()
    logger.info(f'Listening on {management_api_config.host}:{management_api_config.port}.')

    yield

    for task in tasks:
        task.cancel()
        await task

    logger.info('Shutdown xcyber360-apid server.')
