from functools import lru_cache
from fastapi import Depends, Request
from elasticsearch import AsyncElasticsearch

from core.config import settings
from db.elastic import get_elastic
from models.posts import Post
from repositories.base_repository import AbstractStorage
from repositories.post_repository import get_post_repository


class PostService:
    def __init__(self, elastic: AsyncElasticsearch,
                 db: AbstractStorage):
        self.elastic = elastic
        self.db = db

    async def get_posts(self, request: Request) -> list[dict]:
        query = request.query_params.get('query')
        page_number = int(request.query_params.get('page_number', 1))
        page_size = int(request.query_params.get('page_size', 50))
        es_response = await self._get_ids_from_elasticsearch(query, page_number, page_size)
        posts = await self._get_posts_from_postgres_by_id(es_response)
        return posts

    async def _get_ids_from_elasticsearch(self, query: str, page_number: int, page_size: int) -> list[str]:
        from_index = (page_number - 1) * page_size
        template = {
            "from": from_index,
            "size": page_size,
            "query": {
                "match": {
                    "text": query
                }
            }
        }

        response = await self.elastic.search(index=settings.index_name, body=template)
        posts = [el['_source'] for el in response['hits']['hits']]
        ids = [post['id'] for post in posts]
        return ids

    async def _get_posts_from_postgres_by_id(self, ids: list[str]) -> list[dict]:
        result = []
        for post_id in ids:
            response = await self.db.get_one(filter_condition=Post.id == post_id)
            result.append(response)
        return result

    async def delete_post(self, request: Request) -> str:
        post_id = request.path_params.get('post_id')
        await self._delete_post_from_elasticsearch(post_id)
        await self._delete_post_from_postgres(post_id)
        return 'The post has been deleted'

    async def _delete_post_from_elasticsearch(self, post_id: str) -> None:
        post = await self.elastic.exists(index=settings.index_name, id=post_id)
        if not post:
            return None
        await self.elastic.delete(index=settings.index_name, id=post_id)

    async def _delete_post_from_postgres(self, post_id: str) -> None:
        post = await self.db.get_one(filter_condition=Post.id == post_id)
        if not post:
            return None
        await self.db.delete(filter_condition=Post.id == post_id)


@lru_cache()
def get_post_service(
        elastic: AsyncElasticsearch = Depends(get_elastic),
        db: AbstractStorage = Depends(get_post_repository)
) -> PostService:
    return PostService(elastic, db)
