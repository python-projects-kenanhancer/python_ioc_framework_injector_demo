import logging


def handle_general_error_text(e: Exception):
    logging.error(f"An unexpected error occurred: {e}")
