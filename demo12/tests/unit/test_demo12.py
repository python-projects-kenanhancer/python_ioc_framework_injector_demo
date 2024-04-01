import pytest
import logging
import json
from demo12.src.application import EventApplication
from demo12.src.repositories import DatabaseRepository
from demo12.src.serializers import XmlSerializer, JsonSerializer, CsvSerializer
from demo12.src.services import EventServiceClient
from demo12.src.error import (ErrorHandlerFactory,
                              EventServiceError,
                              DatabaseFetchError,
                              SerializeError,
                              XmlSerializeError,
                              JsonSerializeError,
                              CsvSerializeError,
                              handle_database_error_json,
                              handle_event_service_error_text,
                              handle_general_error_text,
                              handle_serialize_error_text,
                              handle_xml_serialize_error_text,
                              handle_xml_serialize_error_json,
                              handle_json_serialize_error_text,
                              handle_json_serialize_error_json,
                              handle_csv_serialize_error_text,
                              handle_csv_serialize_error_json)


class TestDemo12:

    @pytest.fixture
    def database_repository(self):
        return DatabaseRepository()

    @pytest.fixture
    def xml_serializer(self):
        return XmlSerializer()

    @pytest.fixture
    def json_serializer(self):
        return JsonSerializer()

    @pytest.fixture
    def csv_serializer(self):
        return CsvSerializer()

    @pytest.fixture
    def event_service_client(self):
        return EventServiceClient()

    @pytest.fixture
    def xml_serialize_error(self):
        return XmlSerializeError("XML serialization failed", "Missing closing tag", "<user>")

    @pytest.fixture
    def json_serialize_error(self):
        return JsonSerializeError("JSON serialization failed", "No data provided")

    @pytest.fixture
    def csv_serialize_error(self):
        return CsvSerializeError("CSV serialization failed", "No data provided")

    @pytest.fixture
    def app_with_xml_serializer(self, database_repository, xml_serializer, event_service_client):
        return EventApplication(database_repository, xml_serializer, event_service_client)

    @pytest.fixture
    def app_with_json_serializer(self, database_repository, json_serializer, event_service_client):
        return EventApplication(database_repository, json_serializer, event_service_client)

    @pytest.fixture
    def app_with_csv_serializer(self, database_repository, csv_serializer, event_service_client):
        return EventApplication(database_repository, csv_serializer, event_service_client)

    @pytest.fixture
    def error_handler_factory(self):
        error_handler_factory = ErrorHandlerFactory()

        error_handler_factory.register_handler(DatabaseFetchError, handle_database_error_json)
        error_handler_factory.register_handler(SerializeError, handle_serialize_error_text)
        error_handler_factory.register_handler(EventServiceError, handle_event_service_error_text)
        error_handler_factory.register_handler(Exception, handle_general_error_text)

        return error_handler_factory

    def test_xml_serializer_with_falsy_data(self, xml_serializer):
        with pytest.raises(XmlSerializeError) as exc_info:
            xml_serializer.serialize(None)

        assert "XML serialization failed" in str(exc_info.value)
        assert "Missing closing tag" in str(exc_info.value.detail)
        assert "<user>" in str(exc_info.value.element)

    def test_json_serializer_with_falsy_data(self, json_serializer):
        with pytest.raises(JsonSerializeError) as exc_info:
            json_serializer.serialize(None)  # Or other falsy value expected to trigger the error

        assert "JSON serialization failed" in str(exc_info.value)
        assert "No data provided" in str(exc_info.value.detail)

    def test_csv_serializer_with_falsy_data(self, csv_serializer):
        with pytest.raises(CsvSerializeError) as exc_info:
            csv_serializer.serialize(None)  # Or other falsy value expected to trigger the error

        assert "CSV serialization failed" in str(exc_info.value)
        assert "No data provided" in str(exc_info.value.detail)

    def test_handle_xml_serialize_error_text(self, caplog, xml_serialize_error):
        caplog.set_level(logging.ERROR)

        handle_xml_serialize_error_text(xml_serialize_error)

        assert "XML Serialization error occurred" in caplog.text
        assert "XML serialization failed" in caplog.text
        assert "Missing closing tag" in caplog.text

    def test_handle_json_serialize_error_text(self, caplog, json_serialize_error):
        caplog.set_level(logging.ERROR)

        handle_json_serialize_error_text(json_serialize_error)

        assert "JSON Serialization error occurred" in caplog.text
        assert "JSON serialization failed" in caplog.text
        assert "No data provided" in caplog.text

    def test_handle_csv_serialize_error_text(self, caplog, csv_serialize_error):
        caplog.set_level(logging.ERROR)

        handle_csv_serialize_error_text(csv_serialize_error)

        assert "CSV Serialization error occurred" in caplog.text
        assert "CSV serialization failed" in caplog.text
        assert "No data provided" in caplog.text

    def test_app_using_xml_serializer_to_handle_xml_serialize_error_text(self, caplog,
                                                                         app_with_xml_serializer: EventApplication,
                                                                         error_handler_factory):
        caplog.set_level(logging.ERROR)  # Set the logging level to capture ERROR messages

        with pytest.raises(Exception) as e:
            app_with_xml_serializer.run()

        error_handler_factory.register_handler(XmlSerializeError, handle_xml_serialize_error_text)

        error_handler = error_handler_factory.get_handler(e.type)
        error_handler(e.value)

        assert len(caplog.records) == 1  # Ensure only one log message is captured
        log_record = caplog.records[0]
        assert log_record.levelname == 'ERROR'  # Ensure the log level is ERROR
        assert "XML Serialization error occurred" in caplog.text  # Check the message content
        assert "Detail:" in log_record.message  # Check for detail information
        assert "Element:" in log_record.message  # Check for element information

    def test_app_using_json_serializer_to_handle_json_serialize_error_text(self, caplog,
                                                                           app_with_json_serializer: EventApplication,
                                                                           error_handler_factory):
        caplog.set_level(logging.ERROR)  # Set the logging level to capture ERROR messages

        with pytest.raises(Exception) as e:
            app_with_json_serializer.run()

        error_handler_factory.register_handler(JsonSerializeError, handle_json_serialize_error_text)

        error_handler = error_handler_factory.get_handler(e.type)
        error_handler(e.value)

        assert len(caplog.records) == 1  # Ensure only one log message is captured
        log_record = caplog.records[0]
        assert log_record.levelname == 'ERROR'  # Ensure the log level is ERROR
        assert "JSON Serialization error occurred" in caplog.text  # Check the message content
        assert "JSON serialization failed" in caplog.text  # Check the message content
        assert "Detail:" in log_record.message  # Check for detail information

    def test_app_using_csv_serializer_to_handle_csv_serialize_error_text(self,
                                                                         caplog,
                                                                         app_with_csv_serializer: EventApplication,
                                                                         error_handler_factory):
        caplog.set_level(logging.ERROR)  # Set the logging level to capture ERROR messages

        with pytest.raises(Exception) as e:
            app_with_csv_serializer.run()

        error_handler_factory.register_handler(CsvSerializeError, handle_csv_serialize_error_text)
        error_handler = error_handler_factory.get_handler(e.type)
        error_handler(e.value)

        assert len(caplog.records) == 1  # Ensure only one log message is captured
        log_record = caplog.records[0]
        assert log_record.levelname == 'ERROR'  # Ensure the log level is ERROR
        assert "CSV Serialization error occurred" in caplog.text  # Check the message content
        assert "CSV serialization failed" in caplog.text  # Check the message content
        assert "Detail:" in log_record.message  # Check for detail information

    def test_app_using_csv_serializer_to_handle_csv_serialize_error_json(self,
                                                                         caplog,
                                                                         app_with_csv_serializer: EventApplication,
                                                                         error_handler_factory):
        caplog.set_level(logging.ERROR)

        with pytest.raises(Exception) as e:
            app_with_csv_serializer.run()

        error_handler_factory.register_handler(CsvSerializeError, handle_csv_serialize_error_json)
        error_handler = error_handler_factory.get_handler(e.type)
        error_handler(e.value)

        assert len(caplog.records) == 1  # Ensure only one log message is captured
        log_record = caplog.records[0]
        assert log_record.levelname == 'ERROR'  # Ensure the log level is ERROR

        log_message_dict = json.loads(log_record.message)

        # Prepare the expected dictionary for comparison
        expected_dict = {
            "error_type": "CsvSerializationError",
            "message": "CSV serialization failed",
            "detail": "No data provided"
        }

        # Use dictionary comparison for a cleaner assertion
        assert expected_dict.items() <= log_message_dict.items()
