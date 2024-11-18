from contextlib import asynccontextmanager
from logging import getLogger
from typing import AsyncIterator

from httpx import AsyncClient, AsyncHTTPTransport, ConnectError, Timeout, TimeoutException, UnsupportedProtocol

from xcyber360.core.common import ENGINE_SOCKET
from xcyber360.core.engine.events import EventsModule
from xcyber360.core.engine.vulnerability import VulnerabilityModule
from xcyber360.core.exception import Xcyber360EngineError
from xcyber360.core.config.client import CentralizedConfig

logger = getLogger('xcyber360')


class Engine:
    """Xcyber360 Engine API client."""

    def __init__(
        self,
        socket_path: str,
        retries: int,
        timeout: float,
    ) -> None:
        transport = AsyncHTTPTransport(uds=socket_path, retries=retries)
        self._client = AsyncClient(transport=transport, timeout=Timeout(timeout))

        # Engine modules
        self.events = EventsModule(client=self._client)
        self.vulnerability = VulnerabilityModule(client=self._client)

    async def close(self) -> None:
        """Close the Engine client."""
        await self._client.aclose()


@asynccontextmanager
async def get_engine_client() -> AsyncIterator[Engine]:
    """Create and return the engine client.

    Returns
    -------
    AsyncIterator[Engine]
        Engine client iterator.
    """
    engine_config = CentralizedConfig.get_engine_config()
    client = Engine(
        socket_path=engine_config.client.api_socket_path,
        timeout=engine_config.client.timeout,
        retries=engine_config.client.retries
    )

    try:
        yield client
    except TimeoutException:
        raise Xcyber360EngineError(2800)
    except UnsupportedProtocol:
        raise Xcyber360EngineError(2801)
    except ConnectError:
        raise Xcyber360EngineError(2802)
    finally:
        await client.close()
