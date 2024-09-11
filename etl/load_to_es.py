import logging
from elasticsearch import Elasticsearch, helpers

from etl.es_index import INDEX
from src.core.config import Settings

es_settings = Settings()

ELASTICSEARCH = f'http://{es_settings.es_host}:{es_settings.es_port}'


def create_index(elastic_object: Elasticsearch, index_name: str) -> None:
    """Create index."""
    elastic_object.indices.create(index=index_name, ignore=400, body=INDEX)
    logging.info('Индекс успешно создан')


def load_to_es(index_name: str, data: list):
    """Load data to elasticsearch."""
    es = Elasticsearch(ELASTICSEARCH)

    if not es.indices.exists(index=index_name):
        logging.info('Индекс не существет. Создаем индекс.')
        create_index(es, index_name)

    logging.info('Начинается загрузка данных в elasticsearch.')
    actions = []
    for post in data:
        action = {
            "_index": index_name,
            "_id": post.id,
            "_source": post.dict()
        }
        actions.append(action)

    helpers.bulk(es, actions)
    logging.info('Загрузка завершена. Загружено "%s" постов', len(actions))
