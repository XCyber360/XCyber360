from httpx import RequestError
from typing import AsyncGenerator

from xcyber360.core.engine.base import APPLICATION_JSON, APPLICATION_NDJSON, BaseModule
from xcyber360.core.engine.models.base import ErrorResponse
from xcyber360.core.exception import Xcyber360EngineError


class EventsModule(BaseModule):
    """Events module to send stateless events to the Engine."""

    MODULE = 'events'

    async def send(self, event_stream: AsyncGenerator[bytes, None]) -> None:
        """Send events to the engine.
        
        Parameters
        ----------
        event_stream : AsyncGenerator[bytes, None]
            Events as a byte stream.
        """
        try:
            response = await self._client.post(
                url=f'{self.API_URL}/{self.MODULE}/stateless',
                content=event_stream,
                headers={
                    'Accept': APPLICATION_JSON,
                    'Content-Type': APPLICATION_NDJSON,
                }
            )

            if not response.is_success:
                return ErrorResponse(**response.json())

        except RequestError as exc:
            raise Xcyber360EngineError(2803, extra_message=str(exc))
