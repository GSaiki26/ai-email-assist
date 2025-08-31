from aio_pika import Message, connect
from structlog.stdlib import BoundLogger, get_logger

from backend.settings import AMQPSettings

logger: BoundLogger = get_logger()


class AMQPQueue:
    def __init__(self, settings: AMQPSettings) -> None:
        self._settings = settings

    async def send(self, message: bytes) -> None:
        logger.info("sending message to queue...")

        async with await connect(self._settings.dsn.encoded_string()) as conn:
            channel = conn.channel()
            await channel.initialize()

            exchange = channel.default_exchange
            await exchange.publish(Message(message), routing_key=self._settings.queue_name)

        logger.info("message sent to queue.")
