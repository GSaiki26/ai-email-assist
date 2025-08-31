from collections.abc import AsyncGenerator

from aio_pika import connect
from structlog.stdlib import BoundLogger, get_logger

from ai_processor.schemas.email import EmailModel
from ai_processor.settings import AMQPSettings

logger: BoundLogger = get_logger()


class AMQPQueue:
    def __init__(self, settings: AMQPSettings) -> None:
        self._settings = settings

    async def receive(self) -> AsyncGenerator[EmailModel]:
        logger.info("receiving messages from queue...")

        async with await connect(self._settings.dsn.encoded_string()) as conn:
            channel = conn.channel()
            await channel.initialize()

            queue = await channel.get_queue(self._settings.queue_name)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        yield EmailModel.model_validate_json(message.body.decode())
