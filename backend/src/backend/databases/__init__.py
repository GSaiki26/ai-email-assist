from abc import ABC, abstractmethod
from typing import Any

from pydantic import BaseModel


class Database(ABC):
    @abstractmethod
    async def get_page(self, page: int) -> list[dict[str, Any]]:
        raise NotImplementedError

    @abstractmethod
    async def get_total_pages(self) -> int:
        raise NotImplementedError

    @abstractmethod
    async def get_item(self, table_name: str, item_id: str) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def put_item(self, table_name: str, entry: BaseModel) -> dict[str, Any]:
        raise NotImplementedError
