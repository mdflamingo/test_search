from etl.contextmanager import open_postgres_conn_cursor
from etl.models import PostES


def transform_data(dsl: dict) -> list:
    pg_data = get_data_from_postgres(dsl)
    transformed_data = []

    for post in pg_data:
        transformed_data.append(PostES(**post))

    return transformed_data


def get_data_from_postgres(dsl: dict) -> list:
    with open_postgres_conn_cursor(dsl) as pg_cursor:
        query = (
            'SELECT * FROM content.posts'
        )

        pg_cursor.execute(query)
        result = pg_cursor.fetchall()

        return result
