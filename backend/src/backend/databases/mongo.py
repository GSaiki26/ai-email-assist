from typing import Any

from bson import ObjectId
from bson.errors import InvalidId
from pydantic import BaseModel
from pymongo import AsyncMongoClient
from structlog.stdlib import BoundLogger, get_logger

from backend.databases import Database

logger: BoundLogger = get_logger()


class Mongo(Database):
    def __init__(self, uri: str) -> None:
        self._client = AsyncMongoClient(uri)
        self._db = self._client["ai_email_assist"]

    async def get_page(self, page: int) -> list[dict[str, Any]]:
        logger.info("Getting page from MongoDB...", page=page, limit=100)

        skip = (page - 1) * 100
        cursor = self._db["email"].find().skip(skip).limit(100)
        result = await cursor.to_list(length=100)
        for res in result:
            res["_id"] = str(res["_id"])

        logger.info("Page retrieved from MongoDB.", page=page)
        return result

    async def get_total_pages(self) -> int:
        logger.info("Getting total pages from MongoDB...")

        total = await self._db["email"].count_documents({})
        logger.info("Total pages retrieved from MongoDB.", total=total)
        return (total // 100) + 1

    async def get_item(self, table_name: str, item_id: str) -> dict[str, Any]:
        logger.info("Getting item from MongoDB...")

        try:
            ObjectId(item_id)
        except InvalidId as err:
            raise ValueError from err

        res = await self._db[table_name].find_one({"_id": ObjectId(item_id)})
        if not res:
            raise ValueError

        logger.info("Item retrieved from MongoDB", item=res)
        res["_id"] = str(res["_id"])
        return res

    async def put_item(self, table_name: str, entry: BaseModel) -> dict[str, Any]:
        logger.info("Putting item into MongoDB...", entry=entry)

        res = await self._db[table_name].insert_one(entry.model_dump(exclude_none=True))
        logger.info("Item inserted into MongoDB", inserted_id=res.inserted_id)
        return await self.get_item(table_name, res.inserted_id)
