from typing import Any

from aiohttp import ClientError
from structlog.stdlib import BoundLogger, get_logger

from ai_processor.clients.http_client import HTTPClient
from ai_processor.settings import OpenAISettings

logger: BoundLogger = get_logger()


class OpenAI:
    def __init__(self, settings: OpenAISettings) -> None:
        self._settings = settings
        self._client = HTTPClient(
            settings,
            base_url=settings.base_url.encoded_string(),
            headers={
                "Authorization": f"Bearer {settings.api_key.get_secret_value()}",
            },
        )

    async def send(self, message: str) -> list[dict[str, Any]]:
        logger.info("Sending message to OpenAI...", message=message)

        try:
            res = await self._client.send(
                method="POST",
                url="/v1/responses",
                json={"model": self._settings.model, "input": message},
            )

            logger.info("Received response from OpenAI.", status=res.status)
            return (await res.json())["output"]
        except ClientError:
            logger.exception("OpenAI request failed.")
            raise
