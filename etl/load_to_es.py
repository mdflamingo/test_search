import logging

from src.core.config import Settings

es_settings = Settings()

ELASTICSEARCH = f'http://{es_settings.es_host}:{es_settings.es_port}'


def create_index(elastic_object: Elasticsearch, index_name: str) -> None:
    """Создает индекс в elasticsearch."""

    elastic_object.indices.create(index=index_name, ignore=400, body=INDEX)
    logging.info('Индекс успешно создан')


def store_record(index_name: str, data: list):
    """Загрузка данных в elasticsearch."""

    es = Elasticsearch(ELASTICSEARCH)

    if not es.indices.exists(index=index_name):
        logging.info('Индекс не существет. Создаем индекс.')
        create_index(es, index_name)

    logging.info('Начинается загрузка данных в elasticsearch.')
    actions = []
    for movie in data:
        action = {
            "_index": index_name,
            "_id": movie.id,
            "_source": movie.dict()
        }
        actions.append(action)

    helpers.bulk(es, actions)
    logging.info('Загрузка завершена. Загружено "%s" фильмов', len(actions))