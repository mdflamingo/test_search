from functools import lru_cache
from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from db.postgres import get_session

from models.posts import Post
from repositories.base_repository import SQLAlchemyRepository, AbstractStorage


class PostRepository(SQLAlchemyRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.model = Post


@lru_cache()
def get_post_repository(
        session: AsyncSession = Depends(get_session)
) -> AbstractStorage:
    return PostRepository(session)
