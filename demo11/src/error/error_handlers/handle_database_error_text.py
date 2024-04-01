import logging
from ..errors import DatabaseFetchError


def handle_database_error_text(e: DatabaseFetchError):
    logging.error(f"Database error occurred: {e}. Error code: {e.error_code}. Query: {e.query}")
