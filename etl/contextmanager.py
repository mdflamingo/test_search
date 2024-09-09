import logging
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor


@contextmanager
def conn_context_pg(dsl: dict[str, str]):
    pg_conn = psycopg2.connect(**dsl, cursor_factory=DictCursor)
    try:
        logging.info("Creating connection")
        yield pg_conn.cursor()
    finally:
        logging.info("Closing connection")
        pg_conn.commit()
        pg_conn.close()
