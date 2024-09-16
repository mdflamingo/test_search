import logging
from elasticsearch import Elasticsearch, helpers

from es_index import INDEX


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

ELASTICSEARCH = 'http://elasticsearch:9200'


def create_index(elastic_object: Elasticsearch, index_name: str) -> None:
    """Create index."""
    elastic_object.indices.create(index=index_name, ignore=400, body=INDEX)
    logger.info('Индекс успешно создан')


def load_to_es(index_name: str, data: list):
    """Load data to elasticsearch."""
    es = Elasticsearch(ELASTICSEARCH)

    if not es.indices.exists(index=index_name):
        logger.info('Индекс не существует. Создаем индекс.')
        create_index(es, index_name)

    logger.info('Начинается загрузка данных в elasticsearch.')
    actions = []
    for post in data:
        action = {
            "_index": index_name,
            "_id": post.id,
            "_source": post.dict()
        }
        actions.append(action)

    helpers.bulk(es, actions)
    logger.info('Загрузка завершена. Загружено "%s" постов', len(actions))
