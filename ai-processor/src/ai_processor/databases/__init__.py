from abc import ABC, abstractmethod

from pydantic import BaseModel


class Database(ABC):
    @abstractmethod
    async def update_item(self, table_name: str, entry: BaseModel) -> None:
        raise NotImplementedError
