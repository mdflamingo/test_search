from psycopg2.extras import execute_batch

from etl.contextmanager import open_postgres_conn_cursor
from etl.models import PostPG


def load_to_postgres(dsl, data: list) -> None:
    """Load data to postgres."""

    with open_postgres_conn_cursor(dsl) as pg_cursor:
        posts = []
        for row in data:
            dict_row = dict(row)
            post = PostPG(**dict_row)
            posts.append(post)

        values_to_insert = [(str(post.id), str(post.rubrics), str(post.text), str(post.created_date)) for post in posts]

        query = (
            'INSERT INTO posts (id, rubrics, text, created_date) '
            'VALUES (%s,%s,%s,%s) '
            'ON CONFLICT (id) DO NOTHING'
        )
        execute_batch(pg_cursor, query, values_to_insert, page_size=1500)
