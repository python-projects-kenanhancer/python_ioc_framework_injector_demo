from .serializer import Serializer
from ..error.errors import XmlSerializeError


class XmlSerializer(Serializer):
    element = "<user>"

    def serialize(self, data):
        if not data:
            raise XmlSerializeError("XML serialization failed", "Missing closing tag", self.element)
        return f"<data><name>{data['name']}</name><email>{data['email']}</email></data>"
