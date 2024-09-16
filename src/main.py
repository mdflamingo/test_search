import logging
from contextlib import asynccontextmanager

from elasticsearch import AsyncElasticsearch
import uvicorn
from fastapi import FastAPI

from api.v1 import posts_api
from core import config
from db import elastic
from db.postgres import create_database
from core.logger import setup_root_logger


@asynccontextmanager
async def lifespan(fast_api: FastAPI):
    elastic.es = AsyncElasticsearch(hosts=[f'http://{config.settings.es_host}:{config.settings.es_port}'])
    # elastic.es = AsyncElasticsearch(hosts=[f'http://127.0.0.1:{config.settings.es_port}'])

    await create_database()
    yield
    await elastic.es.close()


app = FastAPI(
    lifespan=lifespan,
    title='Text search',
    docs_url='/docs',
    openapi_url='/api/openapi.json',
    description='Поисковик по текстам документов. Данные хранятся в БД по желанию, поисковый индекс в эластике',
    version='0.1.0',
)


app.include_router(posts_api.router, prefix='/api/v1/posts', tags=['posts'])
setup_root_logger()

LOGGER = logging.getLogger(__name__)
LOGGER.info('Starting App')

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
        log_level=logging.INFO,
        reload=True
    )
