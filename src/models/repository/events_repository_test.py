import pytest
from .events_repository import EventsRepository
from src.models.settings.connections import db_connection_handler

db_connection_handler.connect_to_db()


@pytest.mark.skip(reason="Novo registro em banco de dados")
def test_insert_event():
    event = {
        "uuid": "meu-uuid-eh-nois",
        "title": "Evento teste",
        "details": "xama",
        "slug": "slug-teste",
        "maximum_attendees": 666,
    }

    events_repository = EventsRepository()
    response = events_repository.insert_event(event)

    print(response)


def test_get_event_by_id():
    events_repository = EventsRepository()
    response = events_repository.get_event_by_id("meu-uuid-eh-nois")
    print(response)
