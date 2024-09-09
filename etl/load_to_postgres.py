from etl.contextmanager import conn_context_pg
from etl.models import Post


def load_to_postgres(dsl, data: list) -> None:
    with conn_context_pg(dsl) as pg_cursor:
        posts = []
        for row in data:
            dict_row = Post(**row)
            posts.append(dict_row)

        values_to_insert = [(str(post.id), str(post.rubrics), str(post.text), str(post.created_date)) for post in posts]

        query = (
            f'INSERT INTO content.posts (id, rubrics, text, created_date)'
            f'VALUES (%s, %s, %s,  %s)'
            f' ON CONFLICT (id) DO NOTHING')

        pg_cursor.executemany(query, values_to_insert)
