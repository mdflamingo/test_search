import csv
import logging

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def read_csv_file(file_path: str) -> list | None:
    """Reads data from a CSV file."""
    try:
        data = []

        with open(file_path, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                data.append(row)
        return data

    except FileNotFoundError:
        logger.error('Файл не найден.')
        return None

    except csv.Error as e:
        logger.error('Ошибка чтения файла: {}'.format(e))
        return None
