import json
import logging
from ..errors import XmlSerializeError


def handle_xml_serialize_error_json(e: XmlSerializeError):
    error_info = {
        "error_type": "XmlSerializationError",
        "message": str(e),
        "detail": e.detail,
        "element": e.element
    }
    logging.error(json.dumps(error_info))
