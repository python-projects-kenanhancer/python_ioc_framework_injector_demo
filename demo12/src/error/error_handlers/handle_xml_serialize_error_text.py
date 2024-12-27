import logging

from ..errors import XmlSerializeError


def handle_xml_serialize_error_text(e: XmlSerializeError):
    logging.error(
        f"XML Serialization error occurred: {e}. Detail: {e.detail}. Element: {e.element}"
    )
