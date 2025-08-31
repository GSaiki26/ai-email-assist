from bson import ObjectId
from pydantic import BaseModel
from pymongo import AsyncMongoClient
from structlog.stdlib import BoundLogger, get_logger

from ai_processor.databases import Database

logger: BoundLogger = get_logger()


class Mongo(Database):
    def __init__(self, uri: str) -> None:
        self._client = AsyncMongoClient(uri)
        self._db = self._client["email_filter"]

    async def update_item(self, table_name: str, entry: BaseModel) -> None:
        logger.info("Updating item into MongoDB...", entry=entry)

        entry_dict = entry.model_dump(exclude_none=True)
        await self._db[table_name].update_one(
            {"_id": ObjectId(entry_dict.pop("_id", None))},
            {"$set": entry_dict},
        )

        logger.info("Item inserted into MongoDB.")
