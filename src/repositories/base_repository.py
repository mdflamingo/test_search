from abc import ABC, abstractmethod

from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractStorage(ABC):
    @abstractmethod
    async def get_one(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    async def delete(self, **kwargs):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractStorage):

    model = None
    session: AsyncSession = None

    async def get_one(self, filter_condition) -> model:
        stmt = select(self.model).filter(filter_condition)
        result = await self.session.execute(stmt)
        obj = result.scalars().first()

        return obj

    async def delete(self, filter_condition):
        stmt = delete(self.model).filter(filter_condition)
        await self.session.execute(stmt)
        await self.session.commit()
