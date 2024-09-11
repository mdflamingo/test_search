import logging
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor


@contextmanager
def open_postgres_connection(postgres_config):
    """Context manager for postgres connections."""

    connection = psycopg2.connect(**postgres_config, cursor_factory=DictCursor)
    try:
        logging.info("Creating postgres connection")
        yield connection
    finally:
        logging.info("Closing postgres connection")
        connection.commit()
        connection.close()


@contextmanager
def open_postgres_conn_cursor(postgres_config):
    """Context manager for postgres cursor."""

    with open_postgres_connection(postgres_config) as connection:
        cursor = connection.cursor()
        try:
            logging.info("Creating postgres cursor\n")
            yield cursor
        finally:
            logging.info("Closing postgres cursor")
            cursor.close()
