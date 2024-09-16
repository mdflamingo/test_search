import logging

from load_to_es import load_to_es
from extract import read_csv_file
from load_to_postgres import load_to_postgres
from transform import transform_data

DSL = {
    'dbname': 'posts',
    'user': 'postgres',
    'password': 'qwe123',
    'host': 'postgres',
    'port': 5432
}


def main() -> None:
    extracted_data = read_csv_file('data/posts.csv')
    load_to_postgres(DSL, extracted_data)
    transformed_data = transform_data(DSL)
    load_to_es('posts', transformed_data)


if __name__ == '__main__':
    main()
