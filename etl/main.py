from etl.extract import read_csv_file
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


def main():
    extracted_data = read_csv_file('data/posts.csv')
    load_to_postgres(DSL, extracted_data)
    # transformed_data = transform_data(extracted_data[:10])
    # print(transformed_data)


if __name__ == '__main__':
    main()
