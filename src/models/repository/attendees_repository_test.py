import pytest
from .attendees_repository import AttendeesRepository
from src.models.settings.connections import db_connection_handler

db_connection_handler.connect_to_db()


@pytest.mark.skip(reason="Novo registro em banco de dados")
def test_insert_attendee():
    event_id = "meu-uuid-eh-nois"
    attendee_info = {
        "uuid": "attendee_1",
        "name": "name",
        "email": "email@email.com",
        "event_id": event_id,
    }

    repo = AttendeesRepository()
    response = repo.insert_attendee(attendeeInfo=attendee_info)
    print(response)


def test_get_attendee_by_id():
    attendee_id = "attendee_1"
    repo = AttendeesRepository()
    attendee = repo.get_attendee_by_id(attendee_id)

    print(attendee)
