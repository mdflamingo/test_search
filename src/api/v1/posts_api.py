from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Request, Query

from services.post_service import PostService, get_post_service

router = APIRouter()


@router.get('/',
            description='Gets information about all posts',
            status_code=HTTPStatus.OK)
async def posts(request: Request,
                query: Annotated[str, Query(description='Text for posts filtering')],
                page_size: Annotated[int, Query(description='Pagination page size', ge=1)] = 20,
                page_number: Annotated[int, Query(description='Pagination page number', ge=1)] = 1,
                post_service: PostService = Depends(get_post_service)):

    posts = await post_service.get_posts(request)
    if not posts:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='posts not found')
    return posts


@router.delete('/{post_id}/',
               description='Delete post',
               status_code=HTTPStatus.OK)
async def posts(request: Request,
                post_id: str,
                post_service: PostService = Depends(get_post_service)):

    post = await post_service.delete_post(request)
    if not post:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail='posts not found')
    return post
