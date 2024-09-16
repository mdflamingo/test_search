import logging

from etl.extract import read_csv_file
from etl.load_to_es import load_to_es
from etl.load_to_postgres import load_to_postgres
from etl.transform import transform_data
from src.core.config import settings

DSL = {
    'dbname': settings.postgres_db,
    'user': settings.postgres_user,
    'password': settings.postgres_password,
    'host': settings.postgres_host,
    'port': settings.postgres_port
}

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main() -> None:
    logger.info('Starting ETL process...')

    extracted_data = read_csv_file('data/posts.csv')
    load_to_postgres(DSL, extracted_data)
    transformed_data = transform_data(DSL)
    load_to_es(settings.index_name, transformed_data)


if __name__ == '__main__':
    logger.info('Starting ETL process...')
    main()
