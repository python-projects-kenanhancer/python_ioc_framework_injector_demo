import logging

from ..errors import CsvSerializeError


def handle_csv_serialize_error_text(e: CsvSerializeError):
    logging.error(f"CSV Serialization error occurred: {e}. Detail: {e.detail}.")
