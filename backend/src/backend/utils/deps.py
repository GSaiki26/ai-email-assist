from typing import Annotated

from fastapi import Depends

from backend.databases import Database
from backend.databases.mongo import Mongo
from backend.services.queue import AMQPQueue
from backend.settings import Settings


def get_database() -> Database:
    settings = Settings()

    if settings.database.dsn.startswith("mongodb"):
        return Mongo(settings.database.dsn)

    raise NotImplementedError


DatabaseDep = Annotated[Database, Depends(get_database)]


def get_queue() -> AMQPQueue:
    settings = Settings()
    return AMQPQueue(settings.ai_processor_amqp)


AMQPQueueDep = Annotated[AMQPQueue, Depends(get_queue)]
